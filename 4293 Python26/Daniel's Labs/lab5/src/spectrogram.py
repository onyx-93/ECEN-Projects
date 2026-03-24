import numpy as np
import matplotlib.pyplot as plt
from windowing import hann, my_fft, natural_cubic_spline
import sounddevice as sd          # most popular simple choice
import time

def record_audio(duration, fs, channels=1):
    print("\nGet ready to record a 4-second audio clip.")
    for i in range(10, 0, -1):
        print(f"Recording starts in {i}...", end="\r")
        time.sleep(1)
    print("\n>>> SPEAK NOW! <<<")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='float32')
    sd.wait()  # wait until recording is finished
    print("Recording finished.")
    return recording.flatten(), fs   # 1D array, sample rate

if __name__ == "__main__":
    # Record real audio 
    x, fs = record_audio(duration=4, fs=16000)
    t_original = np.arange(len(x)) / fs

    # Cubic Spline Interpolation
    interpolation_factor = 2
    t_interp = np.linspace(0, t_original[-1], len(x) * interpolation_factor)
    x_interp = natural_cubic_spline(t_original, x, t_interp)

    # Use interpolated signal from now on
    x_use = x_interp
    t_use = t_interp
    
    # Spectrogram computation
    N = 1024
    psds = []

    for chunk in hann(x, N):
        
        if len(chunk) != N:
            print("   → short chunk detected (should not happen now)")
            continue
            
        X = my_fft(chunk)[:N//2]
        power = np.abs(X)**2
        psd = 10 * np.log10(power + 1e-12)
        psds.append(psd)

    print('Audio processing ...')
    if psds:
        psds = np.array(psds).T
    else:
        print("No chunks processed!")

    # Time and frequency axes
    original_duration = t_use[-1]  # ≈4.0
    num_times = psds.shape[1]
    times = np.linspace(0, original_duration, num_times)
    freqs = np.linspace(0, fs/2, N//2)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7),
                                   sharex=True, gridspec_kw={'height_ratios': [1, 3]})

    # Top: waveform
    ax1.plot(t_use, x_use, color='C0', lw=0.8)
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Interpolated Audio Waveform")
    ax1.grid(True, alpha=0.3)

    # Bottom: spectrogram
    im = ax2.imshow(psds, aspect='auto', origin='lower',
                extent=[times[0], times[-1], freqs[0], freqs[-1]],
                cmap='magma', vmin=-80, vmax=20, interpolation='bilinear')
    ax2.set_ylabel("Frequency (Hz)")
    ax2.set_xlabel("Time (s)")
    ax2.set_title("Spectrogram (Power Spectral Density, dB)")
    fig.colorbar(im, ax=ax2, label='Power (dB)')
    
    fig.savefig('audio_waveforms.png', dpi=300, bbox_inches='tight')
    print('Plot saved as audio_waveforms.png')
    plt.tight_layout()
    plt.show()