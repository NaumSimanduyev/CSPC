import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
def f(x):   return (x-3)**2 + 1
def df(x):  return 2*(x-3)
def d2f(x): return 2.0

def gradient_descent(df, x, lr, tolerance=0.00001) -> float: #step >= 0.01
    while True:
        if abs(lr*df(x)) < tolerance:
            return x
        x = x - lr*df(x)
        return gradient_descent(df, x, lr)

newton_opt = newton(df, 0, fprime=d2f)
minimize_opt = minimize(f, 0, method="SLSQP")

print(gradient_descent(df, 0, 0.01))
print(newton_opt)
print(float(minimize_opt['x'][0]))

# ---------- 2B: harder landscape ----------
def g(x):   return x**4 - 3*x**2 + x + 5
def dg(x):  return 4*x**3 - 6*x + 1
def d2g(x): return 12*x**2 - 6

newton_opt2 = newton(dg, 2, fprime=d2g)
minimize_opt2 = minimize(g, 2, method="SLSQP")

print(gradient_descent(dg, 2, 0.01))
print(newton_opt2, "minimum" if d2g(newton_opt2) > 0 else "maximum")
print(float(minimize_opt2['x'][0]))
