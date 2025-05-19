'''
File:   audio_to_spectro.py

Spec:   Audio to spectro produces two images per one minute of ingested audio. 
        Each image contains ten, three second spectrogram strips separated by a small 
        black space. Images are roughly square for optimal performance with YOLO. 
        Images are not saved in gray scale for YOLO training purposes. 

I/O:    This program expects one minute audio inputs. 
        This program outputs spetrograms images containing ten spectrogram strips.
        Spectrograms do not overlap each other.

Usage:  python3 audio_transform/audio_to_spectro.py <path/to/audio.wave> -o <output/directory>

Optioanal Args: -ch allows for channel selections, -ds allows for down sampling 
 
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
down_sample_ratio = 1           # Divide the sample rate by this number (--sample_rate)
                                # 2 is the default b/c spectrograms come out cleaner  
chunk_duration = 3              # Number of seconds represented in each pane of the spectrogram
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
desired_sample_rate = sample_rate / down_sample_ratio

# If user wants down sampling, change desired sample rate here TODO: does nothing yet
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

# Determine the number of whole 3 second chunks
samples_per_chunk = int(desired_sample_rate * chunk_duration)
num_chunks = int(len(data) / samples_per_chunk)
print(f"num chunks = {num_chunks}")

all_chunks = [] 
for i in range(num_chunks):
    start_sample = i * samples_per_chunk
    end_sample = start_sample + samples_per_chunk
    chunk_data = data[ start_sample : end_sample ]
    all_chunks.append(chunk_data)

## Create Spectrograms
def make_spectro(num_rows=10, which_plot=0): 
    fig, axes = plt.subplots(
        nrows=num_rows, 
        ncols=1, figsize=(8, 5),
        facecolor='black',
        gridspec_kw={'hspace': -0.5},
        constrained_layout=True)
    
    fig.patch.set_facecolor('black')


    for i in range(num_rows):
        # Compute spectrogram
        fft_size = 1024
        hop_size = fft_size // 2
        window = get_window("hann", fft_size)

                                            # 10 spectros to a plot, if 2nd  spectro grab 10 - 19
        f, t, Sxx = spectrogram(all_chunks[i + which_plot*10], fs=sample_rate, window=window, nperseg=fft_size, scaling='density')

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

    #base_name = os.path.splitext(chunk[0])[0]
    base_name='please work'
    image_name = os.path.join(output_directory, f"{base_name}.jpg")
    plt.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()
    print(f"Saved {image_name}") 


# Make two spectrograms with 
make_spectro(10, 0)
make_spectro(10, 1)





# # Process in chunks of 10
# for chunk_start in range(0, len(10), chunk_size):
#     chunk = files[chunk_start:chunk_start + chunk_size]
#     if len(chunk) < chunk_size: # TODO: skips if there are < 10 audio files to work with
#         break  # Skip incomplete chunks

#     fig, axes = plt.subplots(
#         nrows=chunk_size, 
#         ncols=1, figsize=(8, 5),
#         facecolor='black',
#         gridspec_kw={'hspace': -0.5},
#         constrained_layout=True)
    
#     #fig.patch.set_facecolor('black')

#     for i, file in enumerate(chunk):
#         filename = os.path.join(audio_chunks_dir, file)
#         print(f"Processing {filename}")
#         sample_rate, data = wavfile.read(filename)

#         # Compute spectrogram
#         fft_size = 1024
#         hop_size = fft_size // 2
#         window = get_window("hann", fft_size)

#         f, t, Sxx = spectrogram(data, fs=sample_rate, window=window, nperseg=fft_size, scaling='density')

#         # Focus frequency range
#         fmin, fmax = 3500, 9500
#         freq_slice = np.where((f >= fmin) & (f <= fmax))
#         f = f[freq_slice]
#         Sxx = Sxx[freq_slice, :][0]

#         Sxx_db = 10 * np.log10(Sxx + 1e-10)

#         # Plot
#         ax = axes[i]
#         #ax.set_facecolor('black')  # Set each subplot background to black
#         pcm = ax.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap=plt.cm.binary)
#         ax.set_ylim(4000, 9000)
#         ax.axis('off')
#         # Optinal: induvidual spectrogram labels
#         #ax.text(0, -0.3, file.replace('.wav', ''), va='bottom', ha='left', fontsize=6, transform=ax.transAxes, color='red')

#         # Delete audio chunks
#         os.remove(filename)

#     # Save with the base name of the first spectrogram
#     base_name = os.path.splitext(chunk[0])[0]
#     image_name = os.path.join(output_directory, f"{base_name}.jpg")
#     plt.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=300)
#     plt.close()
#     print(f"Saved {image_name}") 

# sys.exit(0) # Exit happily 