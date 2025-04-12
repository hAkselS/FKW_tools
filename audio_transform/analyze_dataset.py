'''
File:   analyze_dataset.py

Spec:   This program looks into a directory and analyzes a subset
        of wave files in said directory by calling audio_to_spectro.py
        via command line args. This program writes to <analyst_logs.csv>, a csv that indicates
        what files have been previously analyzed and checks to avoid 
        double analyzing the same file. 

Usage: python3 audio_transform/analyze_dataset.py <dataset/path> -o <output/directory> -c <number of wave files to analyze> 
'''

import os 
import argparse 
import csv 
import subprocess
import sys 


###################################################################
# CONFIGURATION DEFAULTS
audio_to_spectro_path = "audio_transform/audio_to_spectro.py"       # This program is a wrapped for audio_to_spectro 
count = 1                                                           # Default number of wave files to analyze
###################################################################
parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="process audio in this directory")
parser.add_argument("-o", "--output", help="choose a location for image outputs") # output directory 
parser.add_argument("-c","--count", type=int, default = 1, 
                    help="count specifies the number of audio files to analyze")
args = parser.parse_args() # TODO: Allow channel and down sampling as args

if not (args.output):
    parser.error("Please specify output directory")

if (args.count):
    count = int(args.count)

i = 0
for  file in sorted(os.listdir(args.input_directory)):
    '''
    Analyze 'count' number of files in a given directory
    '''
    filename = os.path.join(args.input_directory, file)
    if os.path.isfile(filename):
        if (i > args.count): 
            print(f"Max file analysis count [{args.count}] reached, exiting...")
            sys.exit(0)

        with open('audio_transform/analyst_logs/spectrogram_logs.csv', mode='a+', newline='') as spectrogram_logs: 
            # TODO: if this file doesn't exisit, the program will fail
            # TODO: only add once the file has been successfully analyzed 
            spectrogram_logs.seek(0) # Move cursor to the start of the existing data
            reader = csv.reader(spectrogram_logs)

            # Check to see if file has already been analyzed
            if any(row == [filename] for row in reader):
                print(f"Already analyzed [{filename}]")
                continue 
            
            # Add filename if it has not yet been analyzed 
            else: 
                writer = csv.writer(spectrogram_logs)
                writer.writerow([filename])
                print(f"Logged [{filename}] as analyzed")
                i = i + 1 # Only increment i if you have analyzed a file

        # Analyze the file 
        subprocess.run(["python3", audio_to_spectro_path, filename, '-o', args.output], stdout=sys.stdout, stderr=sys.stderr)
        