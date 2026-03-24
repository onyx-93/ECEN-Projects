import numpy as np

def hann(x, window_length=1024, overlap=256, zero_pad=True):
    """Perform Hann windowing on the sampled signal x.

    Given a discrete time series x, yield windowed samples from the time series. The Hann window
    function is applied to reduce tail effects.

    :param x: A numpy array of time-series data. Should have shape (N,1), (1,N), or (N,).
    :param window_length: How many samples to yield in each window. Default 1024.
    :param overlap: How many samples to overlap from one window to the next. Default 256.
    :param zero_pad: Whether to pad the input signal with zeros (front and back). Default True.
    """
    # Silently ignore negative overlap values
    if overlap < 0:
        overlap = 0
    kernel_length = window_length - 2*overlap

    # Zero-pad the data (if requested)
    x = x.reshape((x.size,))
    if zero_pad:
        x = np.concatenate((np.zeros(overlap), x, np.zeros(kernel_length + overlap)))

    # Precompute the Hann windowing function
    W = 1/2 * (1 - np.cos(2*np.pi*np.arange(window_length)/window_length))

    # Yield windowed data segments
    for i in range(x.size // (kernel_length + overlap)):
        t_start = (kernel_length+overlap)*i
        t_end = t_start + window_length
        
        segment = x[t_start:t_end]
        if len(segment) < window_length:
            # Zero-pad the short segment to full length
            segment = np.pad(segment, (0, window_length - len(segment)), mode='constant', constant_values=0)
        
        yield W * segment

def my_fft(x):
    """
    Recursive radix-2 Cooley-Tukey FFT.
    Input x: 1D numpy array of complex or real values, length must be power of 2.
    Returns: complex numpy array (same length)
    """
    x = np.asarray(x, dtype=complex)
    N = x.shape[0]

    if N <= 1:
        return x

    if (N & (N - 1)) != 0:           # not power of 2
        raise ValueError(f"Length must be power of 2, got {N}")

    even = my_fft(x[::2])
    odd  = my_fft(x[1::2])

    factor = np.exp(-2j * np.pi * np.arange(N//2) / N)

    return np.concatenate([
        even + factor * odd,
        even - factor * odd
    ])
    
def natural_cubic_spline(x, y, xnew):
    """
    Natural cubic spline interpolation.
    x, y : original points (must be sorted x)
    xnew : points where we want interpolated values
    Returns: ynew (same shape as xnew)
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xnew = np.asarray(xnew, dtype=float)

    n = len(x) - 1
    if n < 2:
        raise ValueError("Need at least 3 points for cubic spline")

    h = np.diff(x)
    a = y[1:]
    b = np.zeros(n)
    d = np.zeros(n)
    c = np.zeros(n + 1)   # c[0] = c[n] = 0 for natural

    # Build tridiagonal system
    alpha = np.zeros(n)
    for i in range(1, n):
        alpha[i] = (3/h[i])*(a[i]-a[i-1]) - (3/h[i-1])*(a[i-1]-y[i-1])

    l = np.ones(n+1)
    mu = np.zeros(n)
    z = np.zeros(n+1)

    for i in range(1, n):
        l[i] = 2*(x[i+1]-x[i-1]) - h[i-1]*mu[i-1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1]*z[i-1]) / l[i]

    for j in range(n-1, -1, -1):
        c[j] = z[j] - mu[j]*c[j+1]
        b[j] = (a[j]-a[j-1])/h[j] - h[j]*(c[j+1] + 2*c[j])/3
        d[j] = (c[j+1] - c[j]) / (3*h[j])

    # Evaluate on xnew
    ynew = np.zeros_like(xnew)
    for i in range(len(xnew)):
        # Find interval
        idx = np.searchsorted(x, xnew[i]) - 1
        if idx < 0: idx = 0
        if idx >= n: idx = n-1

        dx = xnew[i] - x[idx]
        ynew[i] = y[idx] + b[idx]*dx + c[idx]*dx**2 + d[idx]*dx**3

    return ynew