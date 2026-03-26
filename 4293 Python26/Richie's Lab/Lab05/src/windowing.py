"""Windowing functions for digital signal processing"""

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
        yield W * x[t_start:t_end]
