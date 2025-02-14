import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np

# Reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html

###################################################################
# VARIABLES THAT CHANGE:
wave_file_path = 'short_false_killer_whale_sounds.wav'
desired_channel = 3             # Which channel do you want?
down_sample_tf = True           # Do you want to down sample? 
down_sample_rate = 10           # How muich down sampling?

###################################################################


sample_rate, data = wavfile.read(wave_file_path) # Skips metadata

print(f"sample rate = {sample_rate}")
if len(data.shape) > 1:
    print(f"number of channels = {data.shape[1]}") 
    # If multiple channels, choose channel 4 (Jen's favorite)
    data = data[:, desired_channel]  # Select first channel

else:
    print("error: number of channels must = 1")

if down_sample_tf:
    data = data[::10]                   # Take every 10th sample
    sample_rate = sample_rate // 10     # Adjust the sample rate accordingly
    

length = data.shape[0] / sample_rate
print(f"length = {length}")
time = np.linspace(0, length, data.shape[0])

print(data.shape)

# Plot amplitude vs time
# plt.plot(time, data, label="Left channel")
# plt.xlabel("Time [s]")
# plt.ylabel("Amplitude")
# plt.show()

# Plot spectrogram 
f, t, spectro = signal.spectrogram(data, sample_rate)
spectro_db = 10 * np.log10(spectro + 1e-10)                             # Convert to dB scale, avoid log(0)
plt.pcolormesh(t, f, spectro_db, shading='gouraud', cmap='magma')       # Try plotting in log scale
# plt.pcolormesh(t, f, spectro, shading = 'gouraud')                    # normal

plt.axis("off")
plt.savefig('test1.jpeg', bbox_inches='tight', pad_inches=0)

plt.axis('on')
plt.ylabel('Frequency [Hz]')
plt.ylim(0,15000)
plt.xlabel('Time [sec]')
plt.show()
