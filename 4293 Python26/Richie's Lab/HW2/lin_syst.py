# Ricardo Landeros Aranda | Oklahoma State University
# Spring 2026
# Homework 2 Part 2 | ECEN 4293 Applied Numerical Methods in Python for Engineers
# This code was completed with the use of generative AI, to understand procedures, syntax check 
# and algorithm application.

import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return 25 - x**2 + y**2

def make_T(m):
    T = np.zeros((m, m), dtype=float)
    for i in range(m):
        T[i, i] = -4.0
        if i > 0:
            T[i, i-1] = 1.0
        if i < m-1:
            T[i, i+1] = 1.0
    return T

def make_A(m):
    T = make_T(m)
    I = np.identity(m)
    A = np.zeros((m*m, m*m), dtype=float)

    for block_row in range(m):
        r = block_row * m
        A[r:r+m, r:r+m] = T

        if block_row > 0:
            c = (block_row - 1) * m
            A[r:r+m, c:c+m] = I

        if block_row < m - 1:
            c = (block_row + 1) * m
            A[r:r+m, c:c+m] = I

    return A

def make_b(m):
    h = 2.0 / (m + 1)
    x = np.linspace(-1 + h, 1 - h, m)
    y = np.linspace(-1 + h, 1 - h, m)

    b = np.zeros(m*m, dtype=float)

    for j in range(m):          # y-direction
        for i in range(m):      # x-direction
            k = j * m + i

            # left boundary x = -1
            if i == 0:
                b[k] -= f(-1, y[j])

            # right boundary x = 1
            if i == m - 1:
                b[k] -= f(1, y[j])

            # bottom boundary y = -1
            if j == 0:
                b[k] -= f(x[i], -1)

            # top boundary y = 1
            if j == m - 1:
                b[k] -= f(x[i], 1)

    return b

def cholesky_factor(A):
    n = A.shape[0]
    L = np.zeros_like(A, dtype=float)

    for i in range(n):
        for j in range(i + 1):
            s = np.dot(L[i, :j], L[j, :j])

            if i == j:
                val = A[i, i] - s
                if val <= 0:
                    raise ValueError("Matrix is not positive definite.")
                L[i, j] = np.sqrt(val)
            else:
                L[i, j] = (A[i, j] - s) / L[j, j]

    return L

def forward_sub(L, b):
    n = len(b)
    y = np.zeros(n, dtype=float)
    for i in range(n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
    return y

def backward_sub(U, y):
    n = len(y)
    x = np.zeros(n, dtype=float)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    return x

def solve_heat(m):
    A = make_A(m)
    b = make_b(m)

    # Cholesky requires positive definite matrix, so use -A
    L = cholesky_factor(-A)
    y = forward_sub(L, -b)
    u = backward_sub(L.T, y)

    U = u.reshape((m, m))
    return U

def plot_heatmap(U, m):
    plt.figure(figsize=(6, 5))
    plt.imshow(U, extent=[-1, 1, -1, 1], origin='lower', cmap='hot', aspect='equal')
    plt.colorbar(label='Temperature')
    plt.title(f'Heatmap of u(x,y), m = {m}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.tight_layout()
    plt.show()

# Run for m = 10 and m = 25
for m in [10, 25]:
    U = solve_heat(m)
    print(f"\nm = {m}")
    print("Minimum temperature:", np.min(U))
    print("Maximum temperature:", np.max(U))
    print("Center-closest value:", U[m//2, m//2])
    plot_heatmap(U, m)
