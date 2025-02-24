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

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="process audio in this directory")
parser.add_argument("-o", "--output", help="choose a location for image outputs") # output directory 
args = parser.parse_args()


for i, file in enumerate(sorted(os.listdir(args.input_directory))):
    filename = os.path.join(args.input_directory, file)
    if os.path.isfile(filename):
        print(f"found {filename}")


# Debugging code 
print(f"\nIncoming args:")
print(f"input_directory = [{args.input_directory}]")
print(f"output directory = [{args.output}]")