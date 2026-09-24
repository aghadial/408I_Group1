import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.io
from scipy.io import wavfile

samplerate, data = wavfile.read('human_voice.wav')
print(samplerate)
num_frames = data.shape[0]

print(num_frames)

fig1, ax1 = plt.subplots()

ax1.plot(data)
ax1.set_title("Original Data")

plt.show()


downsize_ratio = 6
downsize_data = np.array([])

for i in range(len(data)):
    if (i % downsize_ratio) == 0:
        downsize_data = np.append(downsize_data, data[i])

print(downsize_data.shape[0])

fig2, ax2 = plt.subplots()
ax2.plot(downsize_data)
ax2.set_title("Downsized Data")
plt.show()

fig, (ax11, ax22) = plt.subplots(2)
ax11.plot(data)
ax22.plot(downsize_data)

# Plot 1 data sample range
x1_start = 30000
x1_end = 30600

# Calculating equivalent sample range for downsized data
x2_start = int( x1_start / downsize_ratio)
x2_end = int( x1_end / downsize_ratio)

ax11.set_xlim(x1_start, x1_end)
ax22.set_xlim(x2_start, x2_end)

ax11.set_title("Original Data")
ax22.set_title("Downsized Data")
plt.tight_layout()

# Showing two plots side by side
plt.show()