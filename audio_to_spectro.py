'''
File:   audio_to_spectro.py

Spec:   Audio to spectro splits audio clips into X second chunks. Chunks are 
        analyzed and transformed into spectrograms with a normalized size.
        Spetrogram images are saved to an 'images' directory. Audio chunks are deleted 
        after use. 

I/O;    This program expects large audio inputs (greater than 3 seconds, up to an hour). 
        This program outputs spetrograms representing 3 seconds of audio data.
        Spectrograms do not overlap each other. Audio clips, an intermediary step, are 
        NOT saved to reduce data clutter.

Usage:  python3 audio_to_spectro.py <path/to/audio.wave>
'''

import matplotlib.pyplot as plt
import os
from scipy.signal import spectrogram, get_window
from scipy.io import wavfile
import numpy as np
from divide_audio import divide_wav_audio
import argparse
import sys 



###################################################################
# VARIABLES THAT CHANGE:
desired_channel = 3             # Which channel do you want?
desired_sample_rate = 500000    # What sample rate do you want? 
output_directory = 'images'

###################################################################
# Accept command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("wave_file_path", help="process this file from audio to spectrograms")
args = parser.parse_args() 

print(f"\nMetadata for [{args.wave_file_path}]:")
audio_file_name = os.path.basename(args.wave_file_path)[:-4] # Get the name of the audio 
print(f"Audio name: [{audio_file_name}]")

try:
    sample_rate, data = wavfile.read(args.wave_file_path)  # Read audio file
except ValueError:
    print("Invalid input file type. Supported file type(s): wav")
    sys.exit(1)

print(f"sample rate = {sample_rate}")

if len(data.shape) > 1:
    print(f"number of channels = {data.shape[1]}")
    data = data[:, desired_channel]  # Select desired channel
else:
    print(f"number of channels = 1")

length = data.shape[0] / sample_rate
print(f"length (seconds) = {length}")

# Divide audio into digestible segments
print(f"\nDividing and downsampling audio:")
audio_chunks_dir = divide_wav_audio(args.wave_file_path, desired_channel, desired_sample_rate, 'audio_chunks')

print("\nGenerating spectrograms")
os.makedirs(output_directory, exist_ok=True)  # Ensure output directory exists

for i, file in enumerate(sorted(os.listdir(audio_chunks_dir))):
    filename = os.path.join(audio_chunks_dir, file)
    if os.path.isfile(filename):
        print(f"Processing {filename}")
        sample_rate, data = wavfile.read(filename)

        # Compute spectrogram using scipy.signal.spectrogram
        fft_size = 1024  # Size of FFT window
        hop_size = fft_size // 2  # 50% overlap
        window = get_window("hann", fft_size)

        f, t, Sxx = spectrogram(data, fs=sample_rate, window=window, nperseg=fft_size,  scaling='density')
        # noverlap=hop_size, (removed overlap)

        # Convert to dB
        Sxx_db = 10 * np.log10(Sxx + 1e-10)

        # Plot and save
        plt.figure(figsize=(8, 6))
        plt.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap='magma')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.ylim(0, 100000)
        #plt.title(f"Spectrogram {i+1}")
        plt.axis("off")
        
        image_name = os.path.join(output_directory, f"{audio_file_name}-{i+1:04d}.jpeg")
        plt.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()
        print(f"Saved {image_name}")
        os.remove(filename)

print(f"Finished processing {audio_file_name}!")

sys.exit(0) # Exit happily
