import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.inspection import permutation_importance
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, r2_score, mean_squared_error, mean_absolute_error

K = 15
DEPTH = 4
T = 0.7

data = pd.read_csv("data/concrete.csv")
X = data.drop(columns="strength")
y = data["strength"]
df = X.assign(strength=y)
print("duplicates:", df.duplicated().sum())
print("missing:\n", df.isna().sum())
df = df.drop_duplicates().reset_index(drop=True)
X = df.drop(columns="strength")
y = df["strength"]
print(df.shape)
print(df.describe().T)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(X["cement"], y, s=8); axes[0].set_xlabel("cement (kg/m3)")
axes[1].scatter(X["age"], y, s=8); axes[1].set_xlabel("age (days)")
for ax in axes:
    ax.set_ylabel("strength (MPa)")
plt.tight_layout()
plt.savefig("results/A2_scatter.png", dpi=150)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("train", X_train.shape, "test", X_test.shape)

def adj_r2(r2, n, p):
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)

lr = LinearRegression().fit(X_train, y_train)
print("intercept", lr.intercept_)
print(pd.Series(lr.coef_, index=X.columns))
pt, pe = lr.predict(X_train), lr.predict(X_test)
r2tr = r2_score(y_train, pt)
print(pd.Series({"train RMSE": np.sqrt(mean_squared_error(y_train, pt)), "test RMSE": np.sqrt(mean_squared_error(y_test, pe)), "test MAE": mean_absolute_error(y_test, pe), "train R2": r2tr, "train adj R2": adj_r2(r2tr, len(X_train), 8), "test R2": r2_score(y_test, pe)}).round(4))
fig, ax = plt.subplots()
ax.scatter(X_test["age"], y_test - pe, s=10)
ax.axhline(0, color="k")
ax.set_xscale("log"); ax.set_xlabel("age (days)"); ax.set_ylabel("residual (MPa)")
plt.savefig("results/A4_residuals.png", dpi=150)

rows = []
for d in [1, 2, 3, 4]:
    poly = make_pipeline(PolynomialFeatures(degree=d, include_bias=False),StandardScaler(), LinearRegression())
    poly.fit(X_train, y_train)
    p = poly[0].n_output_features_
    pt, pe = poly.predict(X_train), poly.predict(X_test)
    r2tr = r2_score(y_train, pt)
    rows.append((d, p, np.sqrt(mean_squared_error(y_train, pt)), np.sqrt(mean_squared_error(y_test, pe)), r2tr, adj_r2(r2tr, len(X_train), p), r2_score(y_test, pe)))
print(pd.DataFrame(rows, columns=["degree", "p", "train RMSE", "test RMSE", "train R2", "train adj R2", "test R2"]).round(4))


y_class = (df["strength"] >= 40).astype(int)
print(y_class.value_counts(normalize=True))
Xc_train, Xc_test, c_train, c_test = train_test_split(X, y_class, test_size=0.2, random_state=42, stratify=y_class)

rows = []
for k in [1, 3, 5, 7, 15, 25, 51, 101]:
    m = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    m.fit(Xc_train, c_train)
    rows.append((k, m.score(Xc_train, c_train), m.score(Xc_test, c_test)))
sw = pd.DataFrame(rows, columns=["K", "train", "test"])
print(sw)
plt.figure()
plt.plot(sw.K, sw.train, "o-", label="train")
plt.plot(sw.K, sw.test, "s-", label="test")
plt.xscale("log")
plt.xlabel("K")
plt.ylabel("accuracy")
plt.legend()
plt.savefig("results/A6_knn_sweep.png", dpi=150)

knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K))
knn.fit(Xc_train, c_train)
knn_raw = KNeighborsClassifier(n_neighbors=K).fit(Xc_train, c_train)
print("with scaler", knn.score(Xc_test, c_test), "without", knn_raw.score(Xc_test, c_test))

accs = []
for rs in range(5):
    a, b, ca, cb = train_test_split(X, y_class, test_size=0.2,random_state=rs, stratify=y_class)
    mm = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K))
    accs.append(mm.fit(a, ca).score(b, cb))
print(accs, np.mean(accs), np.std(accs, ddof=1))

rows = []
for d in [1, 2, 3, 4, 5, 6, 8, None]:
    t = DecisionTreeClassifier(criterion="entropy", max_depth=d, random_state=0)
    t.fit(Xc_train, c_train)
    rows.append((d, t.get_depth(), t.get_n_leaves(), t.score(Xc_train, c_train), t.score(Xc_test, c_test)))
ts = pd.DataFrame(rows, columns=["max_depth", "depth", "leaves", "train", "test"])
print(ts)
plt.figure()
plt.plot(ts.depth, ts.train, "o-", label="train")
plt.plot(ts.depth, ts.test, "s-", label="test")
plt.xlabel("depth")
plt.ylabel("accuracy")
plt.legend()
plt.savefig("results/A6_tree_sweep.png", dpi=150)

tree = DecisionTreeClassifier(criterion="entropy", max_depth=DEPTH, random_state=0)
tree.fit(Xc_train, c_train)
print(export_text(tree, feature_names=list(X.columns), max_depth=2))

def metrics(name, true, pred):
    tn, fp, fn, tp = confusion_matrix(true, pred).ravel()
    return dict(model=name, TP=tp, FP=fp, FN=fn, TN=tn, accuracy=accuracy_score(true, pred), precision=precision_score(true, pred), recall=recall_score(true, pred), F1=f1_score(true, pred))

proba = knn.predict_proba(Xc_test)[:, 1]
final = pd.DataFrame([metrics("KNN", c_test, knn.predict(Xc_test)), metrics("Tree", c_test, tree.predict(Xc_test)), metrics("KNN t=%s" % T, c_test, (proba >= T).astype(int)),]).round(4)
print(final)
final.to_csv("results/A_metrics.csv", index=False)

for t in [0.3, 0.5, 0.7, 0.9]:
    print(t, metrics("t=%s" % t, c_test, (proba >= t).astype(int)))

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
lin = LinearRegression().fit(Xtr, ytr)
pipe = make_pipeline(StandardScaler(), LinearRegression()).fit(Xtr, ytr)
pk = permutation_importance(knn, Xc_test, c_test, scoring="f1", n_repeats=20, random_state=0)
pt = permutation_importance(tree, Xc_test, c_test, scoring="f1", n_repeats=20, random_state=0)
imp = pd.DataFrame({"raw_coef": lin.coef_, "std_coef": pipe[-1].coef_, "tree": tree.feature_importances_, "perm_knn": pk.importances_mean, "perm_tree": pt.importances_mean}, index=X.columns).round(4)
print(imp)
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for ax, col in zip(axes, ["std_coef", "tree", "perm_knn"]):
    s = imp[col].sort_values()
    ax.barh(s.index, s.values); ax.set_title(col)
plt.tight_layout()
plt.savefig("results/A8_importance.png", dpi=150)

rows = []
for d in [1, 2, 3, 4]:
    pm = make_pipeline(PolynomialFeatures(d, include_bias=False), StandardScaler(), LinearRegression()).fit(Xtr, ytr)
    rows.append(("poly %d" % d, pm[0].n_output_features_, r2_score(yte, pm.predict(Xte))))
X1 = X.copy()
X1["age"] = np.log(X1["age"])
X2 = X1.copy()
X2["water"] = X["water"] / (X["cement"] + X["slag"] + X["ash"])
for name, Xa in [("log age", X1), ("log age + w/b", X2)]:
    a, b, ya, yb = train_test_split(Xa, y, test_size=0.2, random_state=42)
    m = LinearRegression().fit(a, ya)
    rows.append((name, Xa.shape[1], r2_score(yb, m.predict(b))))
print(pd.DataFrame(rows, columns=["model", "features", "test_R2"]).round(4))
