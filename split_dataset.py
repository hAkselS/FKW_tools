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

# Get all images that have been annotated into a new directory
def copy_annotated_images_to_tmp(input_directory, input_csv):
    '''
    Move all images with annotations into a temp directory
    ['annotation_id', 'annotator', 'choice', 'created_at', 'id', 'image', 'lead_time', 'updated_at']
    '''
    print(f'input directory = {input_directory}')

    # Make a temporary place for images WITH annotations 
    os.makedirs(output_directory, exist_ok=True)
    if os.path.exists(output_directory):
        print(f'output directory = {output_directory}')
    
    # Move files into temp directory
    df = pandas.read_csv(input_csv)
    if 'image' in df.columns:
        for item in df['image']:
            file_path = os.path.join(input_directory, item)
            if os.path.isfile(file_path): 
                # Move to tmp 
                shutil.copy(file_path, output_directory)
                print(f'Copied [{file_path}] to [{output_directory}]')
            else:
                print(f"File not found: [{file_path}]")



copy_annotated_images_to_tmp(input_directory, input_csv)

# TODO: consider just doing the split here. 