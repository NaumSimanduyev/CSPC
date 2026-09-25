import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

t = list()
x = list()
y = list()
text = np.loadtxt("trajectory.csv", delimiter=",", dtype=str)
for r in text[1:]:
    t.append(float(r[0]))
    x.append(float(r[1]))
    y.append(float(r[2]))

v_x = np.gradient(x, t)
v_y = np.gradient(y, t)
a_x = np.gradient(v_x, t)
a_y = np.gradient(v_y, t)

v = [np.sqrt(v_x[i]**2 + v_y[i]**2) for i in range(len(x))]

fig, axes = plt.subplots(2, 1, figsize=(12, 4.5))

axes[0].plot(x, y)
axes[0].set_xlabel("position x(m)")
axes[0].set_ylabel("position y(m)")

axes[1].plot(t, v)
axes[1].set_ylabel("velocity v(m/s)")
axes[1].set_xlabel("Time t(s)")

plt.tight_layout()
plt.savefig("motion_2D.png")
plt.show()

