import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import numpy as np
import scipy as sp
import math


class_test = np.array([[300, 0.616],
                      [400, 0.525],
                      [500, 0.457]])
def f(x):
    return np.cos(2*np.pi*x)

def vander_itp(array):
    """
    Takes: pts as an array-like shape (n, 2) containing (x_i, y_i)
    Returns: numpy.polynomial.Polynomial interpolant
    """
    pts = np.asarray(array, dtype=float) # Declare a new array with the shape (n, 2)
    x = pts[:, 0] # x_i vector 
    y = pts[:, 1] # y_i vector
    n = len(x) # how many data points are there

    V = np.vander(x, N=n, increasing=True) # Builds a vandermonde matrix from the x values extracted
    coeffs = np.linalg.solve(V, y) # Solve linear system V*c = y

    p = Polynomial(coeffs)  # Create polynomial object that holds coefficients in devreasing degree order

    return p   # Return the solution vector

test = vander_itp(class_test)
val = test(350)

# print(val)
# print(test)
n = 20
x_nodes = np.linspace(0, 2, n)
y_nodes = f(x_nodes)

pts = np.column_stack((x_nodes, y_nodes))
p = vander_itp(pts)

# plt.plot(class_test, label='Class Test Points')
xs_dense = np.linspace(0, 2, 1000)
plt.plot(xs_dense, f(xs_dense), 'k--', label='Cos(2πx)')
plt.plot(xs_dense, p(xs_dense), 'b', label=f'Vander Interpolation degree n = {n}')
plt.scatter(x_nodes, y_nodes, color='red', s=20, label='nodes')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()
