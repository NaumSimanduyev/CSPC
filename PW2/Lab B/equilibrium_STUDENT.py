import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0

def k_imbalance(x): return (2 * x)**2 / ((1 - x) * (1 - x)) - K
x_newt = newton(k_imbalance, 0.5)

def sqr_imbalance(x): return k_imbalance(x)**2
res = minimize(sqr_imbalance, x0=0.5, method="SLSQP", bounds=[(0,0.999999999)])

x_minim = res.x[0]
print(x_minim)
print(x_newt)
print(f"{(x_minim-x_newt):.1e}")

H2_eq = 1 - x_newt
I2_eq = 1 - x_newt
HI_eq = 2*x_newt
print("Equilibrium amounts:")
print("H2", H2_eq)
print("I2", I2_eq)
print("HI", HI_eq)

x_values = np.linspace(0, 0.999, 300)

H2 = 1 - x_values
I2 = 1 - x_values
HI = 2 * x_values

plt.plot(x_values, H2, label="H2")
plt.plot(x_values, I2, label="I2")
plt.plot(x_values, HI, label="HI")
plt.axvline(x_newt, linestyle="--", label=f"Equilibrium x = {x_newt}")

plt.xlabel("Reaction extent x")
plt.ylabel("Amount (mol)")

plt.savefig("equilibrium.png")
plt.show()