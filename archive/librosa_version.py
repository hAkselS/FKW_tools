import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
from scipy.io import wavfile
from divide_audio import divide_wav_audio

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

# Read audio file
sample_rate, data = wavfile.read(args.wave_file_path)  

print(f"\nMetadata for [{args.wave_file_path}]:")
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
        y, sr = librosa.load(filename, sr=desired_sample_rate)

        # Compute Mel spectrogram
        n_fft = 1024  # FFT window size
        hop_length = n_fft // 2  # 50% overlap
        n_mels = 128  # Number of Mel bands
        
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
        S_db = librosa.power_to_db(S, ref=np.max)

        # Plot and save spectrogram
        plt.figure(figsize=(8, 6))
        librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis="time", y_axis="mel", cmap="magma")
        plt.colorbar(format="%+2.0f dB")
        plt.xlabel("Time (s)")
        plt.ylabel("Mel Frequency (Hz)")
        plt.title(f"Mel Spectrogram {i+1}")

        image_name = os.path.join(output_directory, f"mel_spectro_{i+1}.jpeg")
        plt.savefig(image_name, bbox_inches="tight", pad_inches=0, dpi=300)
        plt.close()
        print(f"Saved {image_name}")
# TODO: delete audio chunks after analyzing!!!!!
