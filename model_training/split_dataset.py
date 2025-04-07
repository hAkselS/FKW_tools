'''
File:   split_od_data.py

Spec:   Split object detection data according to YOLO spec. See: https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format
        Remember to export data from label studio in the YOLO OBB format. 

Usage:  python3 split_od_data.py 

'''

import os 
import argparse
import pandas
import shutil

raw_label_dir = '/home/gpu_enjoyer/datasets/FKW_OD_Spectrograms/raw_dataset/labels' # Where unsorted labels are stored
raw_image_dir = '/home/gpu_enjoyer/datasets/FKW_OD_Spectrograms/raw_dataset/images' # Where all images are stored 
output_directory = '/home/gpu_enjoyer/datasets/FKW_OD_Spectrograms/formatted_dataset'

# Create dataset output folder structure
image_train_out = os.path.join(output_directory, 'images/train')
image_val_out = os.path.join(output_directory, 'images/val')
image_test_out = os.path.join(output_directory, 'images/test')
label_train_out = os.path.join(output_directory, 'labels/train')
label_val_out = os.path.join(output_directory, 'labels/val')
label_test_out = os.path.join(output_directory, 'labels/test')

split_ratio = {"train": 0.7, "val": 0.2, "test": 0.1}

# Check that split ratio adds to one
if ( .99 < (split_ratio['train'] + split_ratio['val'] + split_ratio ['test']) < 1.01 ):
    pass
else:
    print("Watch out!!!! your splitt ratio != 1!")
    os._exit(1) 

# Make appropriate directories for output 
os.makedirs(output_directory, exist_ok=True)
if os.path.exists(output_directory):
    print(f'output directory = {output_directory}')
os.makedirs(image_train_out, exist_ok=True)
os.makedirs(image_val_out, exist_ok=True)
os.makedirs(image_test_out, exist_ok=True)
os.makedirs(label_train_out, exist_ok=True)
os.makedirs(label_val_out, exist_ok=True)
os.makedirs(label_test_out, exist_ok=True)

# Copy labels into desired directories
num_annotations = len(os.listdir(raw_label_dir))
print(f'Number of annotations: {num_annotations}')
for i, item in enumerate(os.listdir(raw_label_dir)):
    '''Sort images and labels by copying them into respective directories'''
    # Labels 
    label_name = item 
    input_label_path = os.path.join(raw_label_dir, item)

    # Images
    image_name, _ = os.path.splitext(label_name)  # Remove the .txt extension
    image_name = image_name + '.jpeg'
    input_image_path = os.path.join(raw_image_dir, image_name)

    # Copy to TRAIN 
    if( i < (num_annotations * split_ratio['train']) ):
        # Label
        if os.path.exists(input_label_path):  
            shutil.copy(input_label_path, label_train_out)
        else: 
            print(f"Label_name does not exist: {label_name}")
        # Image 
        if os.path.exists(input_image_path):
            shutil.copy(input_image_path, image_train_out)
        else: 
            print(f"Image_name does not exist: {image_name}")

    # Copy to VALIDATE
    elif( i < (num_annotations * (split_ratio['train'] + split_ratio['val']))): 
        # Label
        if os.path.exists(input_label_path):
            shutil.copy(input_label_path, label_val_out)
        else: 
            print(f"Label_name does not exist: {label_name}")
        # Image 
        if os.path.exists(input_image_path):
            shutil.copy(input_image_path, image_val_out)
        else: 
            print(f"Image_name does not exist: {image_name}")

    # Copy to TEST  
    else:
        # Label
        if os.path.exists(input_label_path):
            shutil.copy(input_label_path, label_test_out)
        else: 
            print(f"Label_name does not exist: {label_name}")
        # Image 
        if os.path.exists(input_image_path):
            shutil.copy(input_image_path, image_test_out)
        else: 
            print(f"Image_name does not exist: {image_name}")

