import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

df = pd.read_csv("Heart_disease_cleveland_new.csv")
print(df.shape)
print(df.head())
age = df['age']
chol = df['chol']
trestbps = df['trestbps']
thalach = df['thalach']
thalach_h = list()
thalach_s = list()
for i, ch, t in zip(range(303), df['thalach'], df['target']):
    if (t == 0):
        thalach_h.append(df['thalach'][i])
    else:
        thalach_s.append(df['thalach'][i])

t_stat, p = st.ttest_ind(thalach_s, thalach_h)

healthy_err = st.sem(thalach_h)
ill_err = st.sem(thalach_s)
healthy_mean = np.mean(thalach_h)
ill_mean = np.mean(thalach_s)
if p < 0.05:
    print("Means are different.", p)
else:
    print("Means are approximately the same.")

print(f"Healthy error: {healthy_err} Healthy mean: {healthy_mean}\nIll error: {ill_err} Ill mean: {ill_mean}")
h_ci = st.t.ppf(0.975, df=len(thalach_h) - 1) * healthy_err
s_ci = st.t.ppf(0.975, df=len(thalach_s) - 1) * ill_err

fig_m, ax_m = plt.subplots(figsize=(5, 5))
ax_m.errorbar([0, 1], [healthy_mean, ill_mean], yerr=[h_ci, s_ci], fmt='o', markersize=8)
ax_m.set_ylabel("max heart rate")
ax_m.set_title("Mean thalach")

fig, axes = plt.subplots(nrows=2,ncols=2, figsize=(10, 8))
axes[0,0].hist(age, color='#d0e8c8', edgecolor="black")
axes[0,1].hist(chol, color='#deb887', edgecolor='black')
axes[1,0].hist(trestbps, color='red', edgecolor='black')
axes[1,1].hist(thalach, color='purple', edgecolor='black')

axes[0,0].set_title("Age")
axes[0,1].set_title("Cholesterol level")
axes[1,0].set_title("Pressure in rest")
axes[1,1].set_title("Max Heart rate")

cols = ['age', 'chol', 'trestbps', 'thalach']
for c in cols:
    print(f"{c}:\n skewness:{st.skew(df[c])}") #skewness 

fig_q, axes_q = plt.subplots(nrows=2, ncols=2, figsize=(10,8)) #q-q plot
st.probplot(df['age'], dist='norm', plot=axes_q[0,0])
axes_q[0,0].set_title('age')
st.probplot(df['chol'], dist='norm', plot=axes_q[0,1])
axes_q[0,1].set_title('chol')
st.probplot(df['trestbps'], dist='norm', plot=axes_q[1,0])
axes_q[1,0].set_title('trestbps')
st.probplot(df['thalach'], dist='norm', plot=axes_q[1,1])
axes_q[1,1].set_title('thalach')

fig_rel, ax_rel = plt.subplots(figsize=(5,5))
ax_rel.scatter(age, thalach)
ax_rel.set_title("Age - Max heart rate relation")

norm_targ = df["target"].value_counts(normalize=True)
print(norm_targ)

plt.tight_layout()
plt.show()