from windowing import hann
import numpy as np
import matplotlib.pyplot as plt
import algs
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import soundfile as sf


if __name__ == "__main__":
    # # Generate a sample noise signal
    # t = np.arange(0.0, 20.5, 0.0005)
    # s1 = np.sin(2*np.pi*100*t)
    # s2 = 2*np.sin(2*np.pi*400*t)
    # s2[t <= 10] = s2[12 <= t] = 0
    # noise = 0.01*np.random.random(size=len(t))
    # x = s1 + s2 + noise
    # TODO: Change this code to record an audio sample instead
    # # Iterate over the windowed audio and compute power spectrum data
    # psds = []
    # N = 1024 # samples per chunk of windowed audio
    # for chunk in hann(x, N):
    #     # Compute the fast Fourier transform (FFT) of this chunk
    #     X_full = algs.fft_recursive(chunk)
    #     X = X_full[0:N//2]
        
    #     # Compute the power spectral density (PSD) of this chunk
    #     # PSD is 10*log10 of the square of the real part of the FFT
    #     psd = 10*np.log10(np.abs(X)**2)
    #     psds.append(psd)
    # psds = np.array(psds).transpose()

    # # Plot the PSDs as a spectrogram
    # # TODO: Add a subplot showing the interpolated audio waveform (with shared x-axis)
    # # TODO: Label and correct the x-axis and y-axis values
    # plt.imshow(psds, aspect='auto', origin='lower')
    # plt.show()

    # ================= This is the audio process part ==================


    # Record, interpolate, and show sample.
    # 1) Load recorded mono audio
    audio_mono, fs = sf.read("record_mono1.wav")   # make sure you saved mono

    # 2) Optionally trim to first few seconds
    max_seconds = 5
    max_samples = int(max_seconds * fs)
    audio_mono = audio_mono[:max_samples]

    # 3) Time axis
    t_original = np.arange(audio_mono.size) / fs

    # 4) Decimate for spline
    step = 200            # tune as needed
    x_short = t_original[::step]
    y_short = audio_mono[::step]

    # 5) New dense grid for plotting waveform
    x_wave = np.linspace(x_short[0], x_short[-1], 5000)
    y_wave = algs.cubic_spline_nak(x_short, y_short, x_wave)
    N = 1024
    psds = []

    for chunk in hann(audio_mono, N):
        X_full = algs.fft_recursive(chunk)
        X = X_full[0:N//2]
        psd = 10 * np.log10(np.abs(X)**2)
        psds.append(psd)

    psds = np.array(psds).T
    fig, (ax_wave, ax_spec) = plt.subplots(2, 1, sharex=True)

    # Top: interpolated waveform
    ax_wave.plot(x_wave, y_wave)
    ax_wave.set_ylabel("Amplitude")

    # Bottom: spectrogram
    im = ax_spec.imshow(
        psds,
        aspect='auto',
        origin='lower',
        extent=[t_original[0], t_original[-1], 0, fs/2]
    )
    ax_spec.set_ylabel("Frequency (Hz)")
    ax_spec.set_xlabel("Time (s)")
    fig.colorbar(im, ax=ax_spec, label="Power (dB)")

    plt.show()