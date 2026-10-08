import numpy as np
import matplotlib.pyplot as plt

Vol = list()
pH = list()
with open("titration.csv", "r", newline=""):
    data = np.loadtxt("titration.csv", delimiter=",", dtype=str)
    for r in data[1:]:
        Vol.append(float(r[0]))
        pH.append(float(r[1]))

slope = np.gradient(pH, Vol)
largest = np.argmax(slope)
print("V_eq:", largest)

plt.plot(Vol, pH)
plt.plot(Vol, slope)

plt.xlabel("Volume(ml)")
plt.ylabel("pH")
plt.axvline(largest, linestyle="--", label="Equivalence point")
plt.savefig("titration.png")
plt.show()