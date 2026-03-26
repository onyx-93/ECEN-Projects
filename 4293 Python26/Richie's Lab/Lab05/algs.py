# FFT Cooley-Tukey Algorithm operates with a complexity in the order of O(Nlog_2(N))
import numpy as np



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
