import numpy as np
from scipy.io.wavfile import read as wav_read

sample_rate_m1, audio_m1 = wav_read("M1.wav")
sample_rate_m2, audio_m2 = wav_read("M2.wav")
sample_rate_m3, audio_m3 = wav_read("M3.wav")

audio_m1 = audio_m1.astype(int)
audio_m2 = audio_m2.astype(int)
audio_m3 = audio_m3.astype(int)

rms_m1 = np.sqrt(np.mean(audio_m1**2))
rms_m2 = np.sqrt(np.mean(audio_m2**2))
rms_m3 = np.sqrt(np.mean(audio_m3**2))

print(f'M1 RMS: {rms_m1}, M2 RMS: {rms_m2}, M3 RMS: {rms_m3}')

r_xy = np.correlate(audio_m1, audio_m2, mode='full')
lags = range(-(len(audio_m2)-1), len(audio_m1))

# This is the code without the builtin function, but it takes too long to run
"""r_xy = []
for m in lags:
    total_sum = 0
    for n in range(len(audio_m1)):
        if 0 <= n-m < len(audio_m2):
            total_sum += audio_m1[n]*audio_m2[n-m]
            r_xy.append(total_sum)"""

max_idx = np.argmax(r_xy)
print(f'Delay: {lags[max_idx] / sample_rate_m1} seconds')