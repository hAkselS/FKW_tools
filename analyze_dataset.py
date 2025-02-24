'''
File:   analyze_dataset.py

Spec:   This program looks into a directory and analyzes a subset
        of wave files in said directory by calling audio_to_spectro.py
        via command line args. This program creates a csv that indicates
        what files have been previously analyzed and checks to avoid 
        double analyzing the same file. 

Usage: python3 analyze_dataset.py <dataset/path> -o <output/directory> -m <metadata/save/path>

'''

