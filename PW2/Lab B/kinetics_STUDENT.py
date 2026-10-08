"""
PW2 Lab B Part 3 -- fit a reaction's rate constant to measured data.

A first-order reaction decays as  C(t) = C0 * exp(-k*t).  You have noisy
concentration-vs-time measurements; find the k that best matches them.
Complete the TODOs. Run:  python kinetics.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

t = list()
c = list()
with open("kinetics.csv", "r", newline=""):
    data = np.loadtxt("kinetics.csv", delimiter=',', dtype=str)
    for r in data[1:]:
        t.append(float(r[0]))
        c.append(float(r[1]))        

c0 = c[0]
def total_error(k): return sum((c - (c0*np.exp(-k*t)))**2)

result = minimize(total_error, 0.5, method="SLSQP", bounds=[(0,5)])
k = result.x[0]
print(k) #fitted k

plt.scatter(t, c, label="Measured data")

t_smth = np.linspace(t[0], t[-1], 200)
fitted = c0*np.exp(-k*t_smth)

plt.plot(t_smth, fitted, label="Fitted curve")
plt.xlabel("Time")
plt.ylabel("Concentration")
plt.legend()
plt.savefig("kinetics.png")
plt.show()
