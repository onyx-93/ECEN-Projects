# Ricardo Landeros Aranda | Oklahoma State University
# ECEN 4293 Numerical Methods in Python for Engineers
# Lab 5 Spring 2026


# The code of this lab was completed using generative AI to write clear and compact code
# as well as a helping tool to understand and implement the FFT and the cubic spline
# Used perplexity pro with the LLM Claude Sonet 4.6

import numpy as np
import matplotlib.pyplot as plt
import scipy as sc


# FFT Cooley-Tukey Algorithm operates with a complexity in the order of O(Nlog_2(N))

def fft_recursive(arr):
    # Initialize array length and base case
    N = len(arr)
    if N == 1:
        return np.array([arr[0]], dtype=complex)
    # Split array into even and odd parts to start recursion
    if N % 2 != 0:
        raise ValueError("\n\tArray length must be a power of 2.\n")

    X_even = fft_recursive(arr[0::2])
    X_odd = fft_recursive(arr[1::2])

    # Recombination of factors (Butterfly) step
    X = np.zeros(N, dtype=complex)
    for k in range(N//2):
        multiplier = np.exp(-2j * np.pi * k/N)
        p = X_even[k]
        q = X_odd[k] * multiplier
        X[k] = p + q
        X[k + N//2] = p - q
    return X

# Interpolation


def cubic_spline_nak(x, y, x_new):
    """
    Natural cubic spline interpolation with not-a-knot bounday conditions.

    Parameters:
    -----------
    x: 1D array, shape (n,)
       Strictly increasing sample positions.
    y: 1D array, shape (n,)
       Sample values at each x.
    x_new: 1D array
       Positions where the spline should be evaluated.

    Returns:
    --------
    y_new: 1D array, same shape as x_new
       Interpolated values at x_new.

    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x_new = np.asarray(x_new, dtype=float)

    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("\n\t x and y must be 1D arrays both the same length.\n")
    
    # 1) Precompute coefficients
    #    - compute h_i = x[i+1] - x[i]
    #    - build and solve linear system for spline parameters
    n = len(x)
    if n < 4:
        raise ValueError("\n\t An array of at least 4 points is needed for a\n\t not a knot cubic spline analysis.\n")
    
    h = np.diff(x)
    a = y[:-1].copy()
    b = np.zeros(n-1)
    c = np.zeros(n-1)
    d = np.zeros(n-1)

    A = np.zeros((n, n))
    rhs = np.zeros(n)

    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        rhs[i] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

    # Left not-a-knot condition at x[1]
    A[0, 0] = h[1] 
    A[0, 1] = -(h[0] + h[1])
    A[0, 2] = h[0]
    rhs[0] = 0.0



    # Right not-a-knot condition at x[n-2]
    A[n - 1, n - 1] = h[-1] 
    A[n - 1, n - 2] = -(h[-2] + h[-1])
    A[n - 1, n - 3] = h[-2]
    rhs[n - 1] = 0.0

    M = np.linalg.solve(A, rhs)

    # 2) Evaluate Spline on x_new, find intervals [x[i], x[i+1]]
    #    and evaluate the corresponding cubic polynomial
    for i in range(n-1):
        hi = h[i]
        a[i] = y[i]
        b[i] = (y[i+1] - y[i]) / hi - (2*M[i] + M[i+1]) * hi / 6.0
        c[i] = M[i] / 2.0
        d[i] = (M[i+1] - M[i]) / (6.0 * hi)

    y_new = np.empty_like(x_new)

    # 3) Return y_new
    # y_new[j] = a[i] + b[i]*u + c[i]*u**2 + d[i]*u**3
    for j, t in enumerate(x_new):
        # Find interval index i with x[i] <= t <= x[i+1]
        i = np.searchsorted(x, t) - 1
        if i < 0:
            i = 0
        if i > n-2:
            i = n-2

        u = t - x[i]
        y_new[j] = a[i] + b[i]*u + c[i]*u**2 + d[i]*u**3

    return y_new

# plt.plot(x, y, "o", label="Data Points")
# plt.plot(x_interp, y_linear(x_interp))
# plt.legend()
# plt.show()

