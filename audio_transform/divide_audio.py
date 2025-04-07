'''
File:   divide_audio.py

Spec:   Functions in this program are called via audio_to_spectro.
        This program should handle all things  audio prep including:
        channel selection, down sampling, and segment sizing. All of
        which may be passed in as arguements. 

Usage:  Do not run this program directly! It is called via audio to spectro. 
'''

from pydub import AudioSegment
import os
import sys 

# Configuration defaults
# input_file = "audio/1705_20170912_170426_960.wav"
output_dir = "audio_chunks"
selected_channel = 0  # 0 for left, 1 for right
target_sample_rate = -1  # Plave holder, this arg should be passed in
segment_length = 3000  # 3 seconds in milliseconds 

def divide_wav_audio(input_audio, 
                 selected_channel=selected_channel, 
                 target_sample_rate=target_sample_rate, 
                 output_dir=output_dir):
    '''
    This function receive a string path to a wave file, 
    strips all but the desired channel, down samples, then splits 
    the audio into small segments and saves them to an output directory. 
    '''

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the audio file
    audio = AudioSegment.from_wav(input_audio)

    # Get the name of the audio 
    audio_file_name = os.path.basename(input_audio)[:-4]
    
    # Select the desired channel if stereo
    if audio.channels > 1:
        audio = audio.split_to_mono()[selected_channel]

    # Downsample to target sample rate
    audio = audio.set_frame_rate(target_sample_rate)
    # audio = audio[::10] # Second downsampling method 

    # Split into 3-second clips and save them
    num_segments = len(audio) // segment_length
    if (num_segments >= 9999):
        print("Error, audio chunks are only allowed values from 0-999. Undefined behaivor!!!")
        sys.exit(1)

    for i in range(num_segments):
        start_time = i * segment_length
        end_time = start_time + segment_length
        segment = audio[start_time:end_time]
        segment.export(f"{output_dir}/{audio_file_name}-{i+1:04d}.wav", format="wav")

    print(f"Processed {num_segments} segments and saved to {output_dir}")
    return (output_dir)