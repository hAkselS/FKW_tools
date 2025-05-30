'''
File:   audio_to_spectro.py

Spec:   Audio to spectro produces two images per one minute of ingested audio. 
        Each image contains ten, three second spectrogram strips separated by a small 
        black space. Images are roughly square for optimal performance with YOLO. 
        Images are not saved in gray scale for YOLO training purposes. 

I/O:    This program expects one minute audio inputs. 
        This program outputs spetrograms images containing ten spectrogram strips.
        Spectrograms do not overlap each other.
        This program currently can ONLY ingest 1 minute audio inputs. 

Usage:  python3 audio_transform/audio_to_spectro.py <path/to/audio.wave> -o <output/directory>

Optioanal Args: -ch allows for channel selections: default channel is 5
'''

import matplotlib.pyplot as plt
import os
from scipy.signal import spectrogram, get_window
from scipy.io import wavfile
import numpy as np
import argparse
import sys 



###################################################################
# CONFIGURATION DEFAULTS
output_directory = 'images'
desired_channel = 5             # Which channel do you want? 5 is default b/c it is furthest from the boat
chunk_duration = 3              # Number of seconds represented in each pane of the spectrogram
freq_min = 3500                 # Spectrogram strip's minimum sampled frequency 
freq_max = 9500                 # Spectrogram strip's maximum sampled frequency 
plot_min = 4000                 # Spectrogram strip's minumum DISPLAYED frequency
plot_max = 9000                 # Spectrogram strip's maximum DISPLAYED frequency
###################################################################
# Accept command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("wave_file_path", help="process this file from audio to spectrograms")
parser.add_argument("-o", "--output", help="choose a location for image outputs") # Output directory 
parser.add_argument("-ch", "--channel", help="select an audio channel to transform") #Channel 
args = parser.parse_args() 

# Use arguement values if they exist
if (args.output):
    output_directory = args.output 
if (args.channel):
    desired_channel = int(args.channel)

print(f"\nMetadata for [{args.wave_file_path}]:")
audio_file_name = os.path.basename(args.wave_file_path)[:-4]    # Get the name of the audio 
print(f"Audio name: [{audio_file_name}]")

try:
    sample_rate, data = wavfile.read(args.wave_file_path)       # Read audio file
except ValueError:
    print("Invalid input file type. Supported file type(s): .wav")
    sys.exit(1)

print(f"Sample rate = {sample_rate}")

# Select a channel if multiple 
if len(data.shape) > 1:
    print(f"number of channels = {data.shape[1]}")
    print(f"sampling from channel: {desired_channel}")
    data = data[:, desired_channel]  # Select desired channel
else:
    print(f"number of channels = 1")

length = data.shape[0] / sample_rate    # Original sample rate 
if not (58 < length < 62): # Make sure length is 60 seconds for now! 
    print(f"Length not ~60 second, undefined behavior... exiting")
    sys.exit(0)
print(f"length (seconds) = {length}")

# Determine the number of whole 3 second chunks
samples_per_chunk = int(sample_rate * chunk_duration)
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
        f, t, Sxx = spectrogram(all_chunks[i + which_plot*10], fs=sample_rate,  window=window, nperseg=fft_size, scaling='density')

        fmin, fmax = freq_min, freq_max
        freq_slice = np.where((f >= fmin) & (f <= fmax))
        f = f[freq_slice]
        Sxx = Sxx[freq_slice, :][0]

        Sxx_db = 10 * np.log10(Sxx + 1e-10)

        # Plot
        ax = axes[i]
        #ax.set_facecolor('black')  # Set each subplot background to black
        pcm = ax.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap=plt.cm.binary)
        ax.set_ylim(plot_min, plot_max)
        ax.axis('off')


    base_name=audio_file_name + '-' + str("{:04}".format(which_plot*10 + 1)) 
    image_name = os.path.join(output_directory, f"{base_name}.jpg")
    plt.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()
    print(f"Saved {image_name}") 

# Make two spectrograms with the input data # TODO: generalize to any # of spectrograms
make_spectro(10, 0)
make_spectro(10, 1)
