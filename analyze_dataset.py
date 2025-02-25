'''
File:   analyze_dataset.py

Spec:   This program looks into a directory and analyzes a subset
        of wave files in said directory by calling audio_to_spectro.py
        via command line args. This program writes to analyst_logs.csv, a csv that indicates
        what files have been previously analyzed and checks to avoid 
        double analyzing the same file. 

Usage: python3 analyze_dataset.py <dataset/path> -o <output/directory>
'''

import os 
import argparse 
import csv 
import subprocess
import sys 

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="process audio in this directory")
parser.add_argument("-o", "--output", help="choose a location for image outputs") # output directory 
parser.add_argument("-c","--count", type=int, default = 1, 
                    help="count specifies the number of audio files to analyze")
args = parser.parse_args()

audio_to_spectro_path = "audio_to_spectro.py"
for i, file in enumerate(sorted(os.listdir(args.input_directory))):
    filename = os.path.join(args.input_directory, file)
    if os.path.isfile(filename):
        if (i > args.count): 
            print(f"Max file analysis count [{args.count}] reached, exiting...")
            sys.exit(0)
        
        
        with open('logs/analyst_logs.csv', mode='a+', newline='') as analyst_logs: 
            analyst_logs.seek(0) # Move cursor to the start of the existing data
            reader = csv.reader(analyst_logs)

            # Check to see if file has already been analyzed
            if any(row == [filename] for row in reader):
                print(f"Already analyzed [{filename}]")
                continue 
            
            # Add filename if it has not yet been analyzed 
            else: 
                writer = csv.writer(analyst_logs)
                writer.writerow([filename])
                print(f"Logged [{filename}] as analyzed")

            

        # Analyze the file 
        subprocess.run(["python3", audio_to_spectro_path, filename], stdout=sys.stdout, stderr=sys.stderr)
        