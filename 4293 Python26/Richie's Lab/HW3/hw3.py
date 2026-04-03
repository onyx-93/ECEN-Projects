# Ricardo Landeros Aranda | Oklahoma State University
# Homework 3 | ECEN 4293 Numerical Methods in Python for Engineers
# Spring 2026

import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import numpy as np
import scipy as sp
import math
from bisection import bisection

# Perplexity was used Claude Sonet 4.6 to understand and apply concepts
# to solve the problems.

# ============================== Problem 1 =================================

def f(x):
    return np.cos(2*np.pi*x)

# Vandermonde interpolation function
def vander_itp(arr):
    """
    Takes: pts as an array-like shape (n, 2) containing (x_i, y_i)
    Returns: numpy.polynomial.Polynomial interpolant
    """
    pts = np.asarray(arr, dtype=float) # Declare a new array with the shape (n, 2)
    x = pts[:, 0] # x_i vector 
    y = pts[:, 1] # y_i vector
    n = len(x) # how many data points are there

    V = np.vander(x, N=n, increasing=True) # Builds a vandermonde matrix from the x values extracted
    coeffs = np.linalg.solve(V, y) # Solve linear system V*c = y

    p = Polynomial(coeffs)  # Create polynomial object that holds coefficients in devreasing degree order

    return p   # Return the solution vector

# ------------------------------ Part a) ------------------------------------
# class_array = np.array([[300, 0.616],
#                       [400, 0.525],
#                       [500, 0.457]])
# desired_point = 350
# class_array_test = vander_itp(class_array)
# val = class_array_test(desired_point)

# print(f"\n\tFor the given array in class when we look for the vandemonde interpolation at the point: {desired_point}")
# print(f"\tWe get the result: {val}.")
# print(f"\n\tFrom the following resultant polynomial: {class_array_test}.\n")


# --------------------------------- Part b) ----------------------------------
# for n in range(1,26,5): # In case of desired constant graphinc uncomment
    # n Number of samples
# n = 9
# x_nodes = np.linspace(0, 2, n)
# y_nodes = f(x_nodes)

# pts = np.column_stack((x_nodes, y_nodes))
# p = vander_itp(pts)

# xs_dense = np.linspace(0, 2, 1000)
# plt.figure(figsize=(12, 8))
# plt.plot(xs_dense, f(xs_dense), 'k--', label='Cos(2πx)')
# plt.plot(xs_dense, p(xs_dense), 'b', label=f'Vander Interpolation degree n = {n}')
# plt.scatter(x_nodes, y_nodes, color='red', s=20, label='nodes')
# plt.legend()
# plt.xlabel('x')
# plt.ylabel('y')
# plt.grid(True)
# plt.show()

# ================================== Problem 2 ====================================

# Lagrange Interpolation function
def lagr_itp(arr):
    """
    arr: array-like of shape (n, 2) with (x_j, y_j)
    returns: numpy.polynomial.Polynomial interpolant in Lagrange form
    """
    pts = np.asarray(arr, dtype=float)
    x = pts[:, 0] # First column, all rows
    y = pts[:, 1] # Second column, all rows
    n = len(x)

    # Declare a zero polynomial
    P = Polynomial([0.0])

    for j in range(n):
        # Indices of all k != j
        idx = [k for k in range(n) if k != j]

        # Polynomial with roots at x_k for k != j:
        # q_j(x) = pi * {k != j} (x - x_k)
        q_j = Polynomial.fromroots(x[idx])

        # Denominator: q_j(x_j) = pi*{k != j} (x_j - x_k)
        denom = np.prod(x[j] - x[idx])

        # L_j(x) = q_j(x) / denom
        L_j = q_j * (1.0/denom)

        # Add y_j * L_j(x) to the interpolant
        P = P + y[j] * L_j

    return P

# For the testing the previous example from problem 1 f(x) = cos(2*pi*x)

# n = 5
# x_nodes = np.linspace(0, 2, n)
# y_nodes = f(x_nodes)

# pts = np.column_stack((x_nodes, y_nodes))
# pv = vander_itp(pts)
# pl = lagr_itp(pts)

# xs_dense = np.linspace(0, 2, 1000)
# plt.figure(figsize=(12, 8))
# plt.plot(xs_dense, f(xs_dense), 'k--', label='Cos(2πx)')
# plt.plot(xs_dense, pv(xs_dense), color="#979797", label=f'Vander Interpolation degree n = {n}')
# plt.plot(xs_dense, pl(xs_dense), color="#363636", linestyle='--', label=f'Lagrange Interpolation degree n = {n}')
# plt.scatter(x_nodes, y_nodes, color='red', s=20, label='nodes')
# plt.legend()
# plt.xlabel('x')
# plt.ylabel('y')
# plt.grid(True)
# plt.show()

# ===================================== Problem 3 =======================================

wave_index_arr = np.array([[6563, 1.50883],
                           [6439, 1.50917],
                           [5890, 1.51124],
                           [5338, 1.51386],
                           [5086, 1.51534],
                           [4861, 1.51690],
                           [4340, 1.52136],
                           [3988, 1.52546]])

lagrange_polynomial = lagr_itp(wave_index_arr)
print(f"\nThe resultant polynomial is: {lagrange_polynomial}\n")

plt.plot(wave_index_arr[:,0], wave_index_arr[:,1], 'bo-')
plt.show()

target = 1.520

def g(lambda_nm):
    return lagrange_polynomial(lambda_nm) - target

a, b = 4861, 4340

result, iterations, roots = bisection(g, a, b)

print(f"Approximate wavelength for refraction index of 1.520: {result}\n")