from pydub import AudioSegment
import os

# Configuration
input_file = "audio/Fake whale sounds.wav"
output_dir = "audio_chunks"
selected_channel = 0  # 0 for left, 1 for right
target_sample_rate = 16000  # Desired downsampling rate
segment_length = 3000  # 3 seconds in milliseconds

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the audio file
audio = AudioSegment.from_wav(input_file)

# Select the desired channel if stereo
if audio.channels > 1:
    audio = audio.split_to_mono()[selected_channel]

# Downsample to target sample rate
audio = audio.set_frame_rate(target_sample_rate)

# Split into 3-second clips and save them
num_segments = len(audio) // segment_length
for i in range(num_segments):
    start_time = i * segment_length
    end_time = start_time + segment_length
    segment = audio[start_time:end_time]
    segment.export(f"{output_dir}/segment_{i+1}.wav", format="wav")

print(f"Processed {num_segments} segments and saved to {output_dir}")
