import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np

sample_rate, data = wavfile.read('/home/gpu_enjoyer/FKW_tools/Fake whale sounds.wav') # Skips metadata

print(f"sample rate = {sample_rate}")
# print(f"number of channels = {data.shape[1]}") # assume one channel cause error 
length = data.shape[0] / sample_rate
print(f"length = {length}")
time = np.linspace(0, length, data.shape[0])

# Plot amplitude vs time
# plt.plot(time, data, label="Left channel")
# plt.xlabel("Time [s]")
# plt.ylabel("Amplitude")
# plt.show()

# Plot spectrogram 
f, t, spectro = signal.spectrogram(data, sample_rate)
plt.pcolormesh(t, f, spectro, shading = 'gouaraud')
plt.ylabel('Frequency [Hz]')
plt.ylim(0,1000)
plt.xlabel('Time [sec]')
plt.show()