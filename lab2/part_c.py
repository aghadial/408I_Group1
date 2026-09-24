from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

sample_rate, audio_data = wavfile.read("Cafe_with_noise.wav") # reading in audio file
time = np.arange(0, len(audio_data)) / sample_rate
plt.figure(figsize=(10, 4))
plt.plot(time, audio_data, lw=0.5)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Audio Waveform") # plot step 1
plt.grid(True)

signal = audio_data.astype(float)
if signal.ndim == 2:
    signal = signal.mean(axis=1)
frequency = np.fft.rfftfreq(len(signal), 1 / sample_rate)
magnitude = np.abs(np.fft.rfft(signal)) / len(signal)
plt.figure(figsize=(10, 4))
plt.plot(frequency, magnitude)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Audio Frequency spectrum") # plot step 2
plt.xlim(0, 5000)
plt.grid(True)

from scipy.signal import butter, sosfiltfilt
cutoff = 1000  # filter cutoff freq 1000 Hz and more
sos = butter(12, cutoff, btype="lowpass", fs=sample_rate, output="sos") # changd the order from 6 to 12 to filter out the beep, butterworth filter
filtered = sosfiltfilt(sos, signal) # prevent phase shift by filtering in both directions

plt.figure(figsize=(10, 4))
plt.plot(time, filtered, lw=0.5)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Filtered Audio")
plt.grid(True)

wavfile.write("filtered_voice.wav", sample_rate, filtered.astype(np.int16)) # save new file
plt.show()