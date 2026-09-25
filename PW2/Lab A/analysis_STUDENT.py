"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

t = list()
y = list()
text = np.loadtxt("freefall.csv", delimiter=",", dtype=str)
for r in text[1:]:
    t.append(float(r[0]))
    y.append(float(r[1]))

velocities = np.gradient(y, t)
accelerations = np.gradient(velocities, t)
acceleration_avg = sum(accelerations)/len(accelerations)
print(acceleration_avg)
print(np.std(accelerations))
velocities_new = cumulative_trapezoid(accelerations, t, initial=0) + velocities[0]
y_new = list(cumulative_trapezoid(velocities_new, t, initial=0) + y[0])
diff = [np.abs(y[i]-y_new[i]) for i in range(len(y))]
print(max(diff))

fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 6))

axes[0].plot(t, y)
axes[0].set_ylabel("position y(m)")

axes[1].plot(t, velocities)
axes[1].set_ylabel("velocity y(m/s)")

axes[2].plot(t, accelerations)
axes[2].axhline(y = -9.81, color="green", linestyle="--", linewidth=1)
axes[2].set_ylabel("acceleration y(m/s^2)")
axes[2].set_xlabel("Time(s)")

plt.savefig("motion.png")
plt.show()

