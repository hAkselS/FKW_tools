'''
File:   split_dataset.py

Spec:   This program will take an directory input. The directory 
        should be mostly filled with images, only a subset need to
        be annotated. This program will split images by train,
        validate, and test. Within each catagory, there will be a
        folder for every class. This program requires the csv option output
        from label studio. 

Usage:  

Output data structure:

root/
    train/
        whistle/
            image_1.jpeg
            image_2.jpeg
        click/
    val/
        whistle/
        click/ 
'''

import os 
import argparse
import pandas
import shutil

# Globals --> args (TODO) 
input_directory = '/images' # TODO: fix before use 
input_csv = 'annotations_output.csv'
output_directory = 'temporary_image_directory'

split_ratio = {"train": 0.7, "val": 0.2, "test": 0.1}
catagories = ['whistle', 'click']

# Get all images that have been annotated into a new directory

'''
['annotation_id', 'annotator', 'choice', 'created_at', 'id', 'image', 'lead_time', 'updated_at']
'''
print(f'input directory = {input_directory}')

# Make a temporary place for images WITH annotations 
os.makedirs(output_directory, exist_ok=True)
if os.path.exists(output_directory):
    print(f'output directory = {output_directory}')

# Move files into temp directory
df = pandas.read_csv(input_csv)
# TODO: need to create a cascade filter here
# if is file, if is catagory, move tmp location
# determine counts of each class from tmp location
# move from temp location to final file structure 
if 'image' in df.columns:
    for item in df['image']:
        file_path = os.path.join(input_directory, item)
        if os.path.isfile(file_path): 
            # Move to tmp 
            shutil.copy(file_path, output_directory)
            print(f'Copied [{file_path}] to [{output_directory}]')
        else:
            print(f"File not found: [{file_path}]")




