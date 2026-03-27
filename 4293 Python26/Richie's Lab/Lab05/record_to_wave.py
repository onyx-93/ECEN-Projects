import sounddevice as sd
import soundfile as sf
import numpy as np

def record_to_wav(filename="record_mono.wav"):
    fs = int(input("\n\tEnter sampling rate in Hz (44100–48000): "))
    duration = int(input("\n\tEnter recording duration in seconds (5–10): "))

    if fs < 44100 or fs > 48000:
        raise ValueError(f"\nSampling rate ({fs}) Hz outside 44100–48000.\n")
    if duration < 5 or duration > 10:
        raise ValueError(f"\nDuration ({duration}) s outside 5–10.\n")

    print("\n\tRecording...")
    rec = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float32')
    sd.wait()
    print("\n\tRecording finished.\n")

    audio_mono = rec[:, 0]          # take left channel
    sf.write(filename, audio_mono, fs)
    print(f"\tSaved to {filename}")
    return filename, fs

if __name__ == "__main__":
    record_to_wav()


# =================== Dirty sketch to record sound ============================= 

# Audio recording
# Values to utilize

# freq = int(input("\n\tEnter the desired frequency to do the sampling in Hz (44100 - 48000): "))
# duration = int(input("\n\tProvide the desired sample duration in seconds (5 - 10): "))

# if freq < 44100 or freq > 48000:
#     raise ValueError(f"\nFrequency value ({freq})Hz outside of the range, please provide a value within the range.\n")

# if duration < 5 or duration > 10:
#     raise ValueError(f"\nRecord duration value ({duration})s outside of the range, please provide a value within the range.\n")

# print("\n\tRecording...\n")

# # Start recorder

# recording = sd.rec(duration * freq, samplerate = freq, channels = 2, dtype='float32')

# # Record audio

# sd.wait()

# print("\n\tRecording finished.\n")

# audio_mono = recording[:, 0]

# sf.write("record_mono.wav", audio_mono, freq)

# t_original = np.arange(audio_mono.size) / freq
# t_interp = np.linspace(t_original, t_original[-1], audio_mono.size) / N
# audio_interp = algs.cubic_spline_nak(t_original, audio_mono, t_interp)
