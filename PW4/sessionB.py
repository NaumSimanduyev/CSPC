import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing  import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

wine = load_wine(as_frame=True)
X = wine.data
cultivar = wine.target
print(wine.DESCR)
print(X.describe().T)

pca_raw = PCA().fit(X)
print(pca_raw.explained_variance_ratio_[0])
print(pd.Series(pca_raw.components_[0], index=X.columns).sort_values(key=abs, ascending=False))

scaler = StandardScaler()
Z = scaler.fit_transform(X)
print(Z.mean(axis=0).round(6), Z.std(axis=0))
pca = PCA().fit(Z)
evr = pca.explained_variance_ratio_
cum = np.cumsum(evr)
print(pd.DataFrame({"evr": evr, "cumulative": cum}).round(4))
plt.figure()
plt.bar(range(1, 14), evr)
plt.plot(range(1, 14), cum, "o-", color="C1")
plt.axhline(0.9, color="k", ls="--")
plt.xlabel("component"); plt.ylabel("explained variance ratio")
plt.savefig("results/B3_scree.png", dpi=150)
load = pd.DataFrame(pca.components_[:2].T, index=X.columns, columns=["PC1", "PC2"])
print(load.sort_values("PC1").round(3))
print(load.sort_values("PC2").round(3))
scores = pca.transform(Z)
plt.figure()
plt.scatter(scores[:, 0], scores[:, 1], s=18, color="gray")
plt.xlabel("PC1"); plt.ylabel("PC2")
plt.savefig("results/B3_pca_scatter.png", dpi=150)

print([KMeans(3, n_init=1, random_state=rs).fit(Z).inertia_ for rs in range(8)])
print(KMeans(3, n_init=10, random_state=0).fit(Z).inertia_)
inert = [KMeans(k, init="k-means++", n_init=10, random_state=0).fit(Z).inertia_ for k in range(1, 11)]
print(inert)
plt.figure()
plt.plot(range(1, 11), inert, "o-")
plt.xlabel("k"); plt.ylabel("inertia")
plt.savefig("results/B4_elbow.png", dpi=150)

km = KMeans(n_clusters=3, init="k-means++", n_init=10, max_iter=300, random_state=0)
km.fit(Z)
print(np.bincount(km.labels_))
print(pd.DataFrame(scaler.inverse_transform(km.cluster_centers_), columns=X.columns).round(2).T)
plt.figure()
plt.scatter(scores[:, 0], scores[:, 1], c=km.labels_, s=18)
plt.xlabel("PC1"); plt.ylabel("PC2")
plt.savefig("results/B5_pca_clusters.png", dpi=150)

rows = []
for name, data in [("scaled", Z), ("raw", X.values), ("PC1+PC2", scores[:, :2])]:
    labels = KMeans(3, n_init=10, random_state=0).fit(data).labels_
    table = pd.crosstab(cultivar, labels)
    print(name); print(table)
    rows.append((name, table.max(axis=0).sum() / len(cultivar)))
agr = pd.DataFrame(rows, columns=["version", "agreement"])
print(agr)
agr.to_csv("results/B_agreement.csv", index=False)


Xtr, Xte, ytr, yte = train_test_split(X, cultivar, test_size=0.25, random_state=42, stratify=cultivar)
m1 = make_pipeline(StandardScaler(), KNeighborsClassifier(5)).fit(Xtr, ytr)
m2 = make_pipeline(StandardScaler(), PCA(n_components=2), KNeighborsClassifier(5)).fit(Xtr, ytr)
print(m1.score(Xte, yte), m2.score(Xte, yte))
