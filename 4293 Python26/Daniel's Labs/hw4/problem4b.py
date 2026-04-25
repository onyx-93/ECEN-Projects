
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 8*x**8 - 12*x**7 - 62*x**6 + 89*x**5 + 156*x**4 - 215*x**3 - 126*x**2 + 186*x

def five_point_midpoint(f, h):
    def derivative(x):
        return (f(x - 2*h) - 8*f(x - h) + 8*f(x + h) - f(x + 2*h)) / (12 * h)
    return derivative

def f_prime_exact(x):
    return 64*x**7 - 84*x**6 - 372*x**5 + 445*x**4 + 624*x**3 - 645*x**2 - 252*x + 186


# Part C plotting

# x range
x = np.linspace(-2, 2, 400)

# step sizes
h1 = 1/2
h2 = 1/16

# numerical derivatives
df_h1 = five_point_midpoint(f, h1)
df_h2 = five_point_midpoint(f, h2)

# plot
plt.figure()

plt.plot(x, f_prime_exact(x), label="Analytical", color='blue', linewidth=2)
plt.plot(x, df_h1(x), '--', color='black', label="5-point h = 1/2")
plt.plot(x, df_h2(x), '--', color='red', label="5-point h = 1/16", linewidth=2)

plt.xlabel("x")
plt.ylabel("f'(x)")
plt.title("Analytical vs Numerical Derivative")
plt.legend()
plt.grid()

plt.show()