import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

df = pd.read_csv("./chemicals_cancer.csv")
for c in ["benzene", "cadmium"]:
    r, p = st.pearsonr(df[c], df["malignancy"])
    rho, p_rho = st.spearmanr(df[c], df["malignancy"])
    print(f"{c}: Pearson r = {r:.3f}, Spearman rho = {rho:.3f}")

restr = df[(df["pollution_index"] > 40) & (df["pollution_index"] < 60)]
print("n =", len(restr))
for c in ["benzene", "cadmium"]:
    r, p = st.pearsonr(restr[c], restr["malignancy"])
    print(f"{c}: r = {r:.3f}")


def resid(y, x):
    return y - np.polyval(np.polyfit(x, y, 1), x)

for c in ["benzene", "cadmium"]:
    r, p = st.pearsonr(resid(df[c], df["pollution_index"]),
                       resid(df["malignancy"], df["pollution_index"]))
    print(f"partial {c}: r = {r:.3f}")

for k in ["benzene", "cadmium", "malignancy"]:
    r_age, p_age = st.pearsonr(df[c], df["age"])
    print(f"partial {c} (for age): r = {r:.3f}")