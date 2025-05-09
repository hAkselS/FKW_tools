'''
File:   audio_to_spectro.py

Spec:   Audio to spectro splits audio clips into 3 second chunks. Chunks are 
        analyzed and transformed into spectrograms with a normalized size.
        Spetrogram images are saved to an 'images' directory. Audio chunks are deleted 
        after use. 

I/O:    This program expects large audio inputs (greater than 3 seconds, up to an hour). 
        This program outputs spetrograms representing 3 seconds of audio data.
        Spectrograms do not overlap each other. Audio clips, an intermediary step, are 
        NOT saved to reduce data clutter.

        Input: <.wav> file
        Output: <.jpeg> files in <FKW_tools/images>

Usage:  python3 audio_transform/audio_to_spectro.py <path/to/audio.wave> -o <output/directory>
 
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
# CONFIGURATION DEFAULTS
output_directory = 'images'
desired_channel = 5             # Which channel do you want? 5 is default b/c it is furthest from the boat
down_sample_ratio = 2           # Divide the sample rate by this number (--sample_rate)
                                # 2 is the default b/c spectrograms come out cleaner  
###################################################################
# Accept command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("wave_file_path", help="process this file from audio to spectrograms")
parser.add_argument("-o", "--output", help="choose a location for image outputs") # Output directory 
parser.add_argument("-ch", "--channel", help="select an audio channel to transform") #Channel 
parser.add_argument("-ds", "--down_sample", help="down sample by a factor of <user input>") # TODO: ensure 1 and above
args = parser.parse_args() 

# Use arguement values if they exist
if (args.output):
    output_directory = args.output 
if (args.channel):
    desired_channel = int(args.channel)

print(f"\nMetadata for [{args.wave_file_path}]:")
audio_file_name = os.path.basename(args.wave_file_path)[:-4] # Get the name of the audio 
print(f"Audio name: [{audio_file_name}]")

try:
    sample_rate, data = wavfile.read(args.wave_file_path)  # Read audio file
except ValueError:
    print("Invalid input file type. Supported file type(s): .wav")
    sys.exit(1)

print(f"native sample rate = {sample_rate}")
desired_sample_rate = sample_rate

# If user wants down sampling, change desired sample rate here
if (args.down_sample):
    down_sample_ratio = float(args.down_sample)
    desired_sample_rate = int(desired_sample_rate / down_sample_ratio)

# DEBUG 
print(f"desired sample rate = {desired_sample_rate}")


# Select a channel if multiple 
if len(data.shape) > 1:
    print(f"number of channels = {data.shape[1]}")
    print(f"sampling from channel: {desired_channel}")
    data = data[:, desired_channel]  # Select desired channel
else:
    print(f"number of channels = 1")

length = data.shape[0] / sample_rate
print(f"length (seconds) = {length}")

# Divide audio into digestible segments
print(f"\nDividing and downsampling audio:")
audio_chunks_dir = divide_wav_audio(args.wave_file_path, desired_channel, desired_sample_rate, 'audio_chunks')

# Create output directory 
print("\nGenerating spectrograms")
os.makedirs(output_directory, exist_ok=True)  # Ensure output directory exists

## Create Spectrograms
# Identify files 
files = sorted([f for f in os.listdir(audio_chunks_dir) if os.path.isfile(os.path.join(audio_chunks_dir, f))])
chunk_size = 10

# Process in chunks of 10
for chunk_start in range(0, len(files), chunk_size):
    chunk = files[chunk_start:chunk_start + chunk_size]
    if len(chunk) < chunk_size: # TODO: skips if there are < 10 audio files to work with
        break  # Skip incomplete chunks

    fig, axes = plt.subplots(
        nrows=chunk_size, 
        ncols=1, figsize=(8, 5),
        facecolor='black',
        gridspec_kw={'hspace': -0.5},
        constrained_layout=True)
    
    #fig.patch.set_facecolor('black')

    for i, file in enumerate(chunk):
        filename = os.path.join(audio_chunks_dir, file)
        print(f"Processing {filename}")
        sample_rate, data = wavfile.read(filename)

        # Compute spectrogram
        fft_size = 1024
        hop_size = fft_size // 2
        window = get_window("hann", fft_size)

        f, t, Sxx = spectrogram(data, fs=sample_rate, window=window, nperseg=fft_size, scaling='density')

        # Focus frequency range
        fmin, fmax = 3500, 9500
        freq_slice = np.where((f >= fmin) & (f <= fmax))
        f = f[freq_slice]
        Sxx = Sxx[freq_slice, :][0]

        Sxx_db = 10 * np.log10(Sxx + 1e-10)

        # Plot
        ax = axes[i]
        #ax.set_facecolor('black')  # Set each subplot background to black
        pcm = ax.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap=plt.cm.binary)
        ax.set_ylim(4000, 9000)
        ax.axis('off')
        # ax.text(0.5, -0.15, file.replace('.wav', ''), va='top', ha='center',
        #     fontsize=6, color='white', transform=ax.transAxes)
        #ax.text(0, -0.3, file.replace('.wav', ''), va='bottom', ha='left', fontsize=6, transform=ax.transAxes, color='red')

        # Optional: delete original audio
        os.remove(filename)

    # Save with the base name of the first spectrogram
    base_name = os.path.splitext(chunk[0])[0]
    image_name = os.path.join(output_directory, f"{base_name}.jpg")
    plt.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()
    print(f"Saved {image_name}") 

# for i, file in enumerate(sorted(os.listdir(audio_chunks_dir))):
#     filename = os.path.join(audio_chunks_dir, file)
#     if os.path.isfile(filename):
#         print(f"Processing {filename}")
#         sample_rate, data = wavfile.read(filename)

#         # Compute spectrogram using scipy.signal.spectrogram
#         fft_size = 1024  # Size of FFT window
#         hop_size = fft_size // 2  # 50% overlap
#         window = get_window("hann", fft_size)

#         f, t, Sxx = spectrogram(data, fs=sample_rate, window=window, nperseg=fft_size,  scaling='density')

#         # Remove all but the 4k-9k Hz range  
#         fmin = 3500 # Hz
#         fmax = 9500 # Hz
#         freq_slice = np.where((f >= fmin) & (f <= fmax))
#         f   = f[freq_slice]
#         Sxx = Sxx[freq_slice,:][0]   
             
#         # Convert to dB
#         Sxx_db = 10 * np.log10(Sxx + 1e-10)


#         # Plot
#         fig, axes = plt.subplots(nrows=10, ncols=1, figsize=(8, 5),  # 10 x 0.3 + small gaps ~ 2 units
#                          constrained_layout=True)

#         for i, ax in enumerate(axes):
#             pcm = ax.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap=plt.cm.binary)
#             ax.set_ylim(4000, 9000)
#             ax.axis('off')

#             # Caption: Adjust or customize as needed
#             ax.text(-0.01, 0.5, f"Spectrogram {i+1}", va='center', ha='right', fontsize=8, transform=ax.transAxes)


#         # Save and remove audio 
#         image_name = os.path.join(output_directory, f"{audio_file_name}-{i+1:04d}.jpg")
#         plt.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=300)
#         plt.close()
#         print(f"Saved {image_name}")
#         os.remove(filename)

# print(f"Finished processing {audio_file_name}!")

# sys.exit(0) # Exit happily
