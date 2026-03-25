from windowing import hann
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Generate a sample noise signal
    t = np.arange(0.0, 20.5, 0.0005)
    s1 = np.sin(2*np.pi*100*t)
    s2 = 2*np.sin(2*np.pi*400*t)
    s2[t <= 10] = s2[12 <= t] = 0
    noise = 0.01*np.random.random(size=len(t))
    x = s1 + s2 + noise
    # TODO: Change this code to record an audio sample instead

    # Iterate over the windowed audio and compute power spectrum data
    psds = []
    N = 1024 # samples per chunk of windowed audio
    for chunk in hann(x, N):
        # Compute the fast Fourier transform (FFT) of this chunk
        X = np.fft.fft(chunk)[0:N//2] # TODO: Use your own FFT instead

        # Compute the power spectral density (PSD) of this chunk
        # PSD is 10*log10 of the square of the real part of the FFT
        psd = 10*np.log10(np.abs(X)**2)
        psds.append(psd)
    psds = np.array(psds).transpose()

    # Plot the PSDs as a spectrogram
    # TODO: Add a subplot showing the interpolated audio waveform (with shared x-axis)
    # TODO: Label and correct the x-axis and y-axis values
    plt.imshow(psds, aspect='auto', origin='lower')
    plt.show()



"""    # --------------- Optional: interpolate waveform ----------------
    # Example: interpolate to 2× denser points
    interpolation_factor = 2
    t_interp = np.linspace(0, t_original[-1], len(x) * interpolation_factor)
    x_interp = natural_cubic_spline(t_original, x, t_interp)

    # Use interpolated version from now on (or keep original — up to you)
    #x_use = x_interp
    #t_use = t_interp
    # If you skip interpolation → x_use = x; t_use = t_original"""