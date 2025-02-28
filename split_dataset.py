'''
File:   split_dataset.py

Spec:   This program will take an directory input. The directory 
        should be mostly filled with images, only a subset need to
        be annotated. This program will split images by train,
        validate, and test. Within each catagory, there will be a
        folder for every class. This program requires the csv-output
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
output_directory = 'FKW_training_data'

split_ratio = {"train": 0.7, "val": 0.2, "test": 0.1}
catagories = ['whistle', 'click']

'''
['annotation_id', 'annotator', 'choice', 'created_at', 'id', 'image', 'lead_time', 'updated_at']
'''
print(f'input directory = {input_directory}')

 # 
# os.makedirs(output_directory, exist_ok=True)
# if os.path.exists(output_directory):
#     print(f'output directory = {output_directory}')

# Look at the dataset, determine number of each class 

df = pandas.read_csv(input_csv)

print(df.columns)

whistle_images = df.loc[df['choice'] == 'whistle', 'image'].tolist()
click_images = df.loc[df['choice'] == 'click', 'image'].tolist()
whistle_click_images = df.loc[df['choice'].str.contains('"whistle"' and '"click"', na=False), 'image']


print(f'Number of whistle images: {len(whistle_images)}')
print(f'Number of click images: {len(click_images)}')
print(f'Number of whistle & click images: {len(whistle_click_images)}')