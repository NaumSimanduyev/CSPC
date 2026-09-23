"""
PW1 Lab B -- read observed decay data and compare it to the analytical law.
Produce a 1x2 figure:  left = observed data,  right = analytical N0*exp(-lam*t),
with SHARED axes so the two shapes are directly comparable.

Complete the TODOs below. Run with:  python plot.py
"""

import numpy as np
from matplotlib import pyplot as plt
import csv

LAMBDA = 0.3     # decay constant, given

t = list()
observed = list()
analytical = list()
with open("decay_observed.csv", "r", newline="") as f:
    data = np.loadtxt("decay_observed.csv", delimiter=',', dtype=str)
    for r in data[1:]:
        t.append(float(r[0]))
        observed.append(float(r[1]))

N0 = observed[0]

for i in range(len(observed)):
    analytical.append(N0*np.exp(-LAMBDA*t[i])) 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), sharex=True, sharey=True)
ax1.scatter(t, observed, color="tab:green", label="Observed")
ax1.set_title('Observed data')
ax1.set_ylabel("The amount of atoms(N)")
ax1.set_xlabel("Time(s)")

ax2.plot(t, analytical, color='tab:blue',label='Analytical Data')
ax2.set_title('Analytical fit')
ax2.set_xlabel('Time(s)')

fig.suptitle('Decay: Observed vs Analytical')

plt.savefig("figure.png")
plt.show()

# TODO 4: save the figure as figure.png
