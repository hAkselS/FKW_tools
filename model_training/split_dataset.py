'''
File:   split_od_data.py

Spec:   Split object detection data according to YOLO spec. See: https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format
        Remember to export data from label studio in the YOLO OBB format. 
        
Usage:  python3 split_od_data.py <path/to/labels> <path/to/images> -o <output/directory> 

'''

import os 
import argparse
import pandas
import shutil
import sys

###################################################################
# CONFIGURATION DEFAULTS
output_directory = 'split_outputs'
split_ratio = {"train": 0.7, "val": 0.2, "test": 0.1}
###################################################################

# Accept command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("labels", help="what directory of the YOLO OBB labels stored in?")
parser.add_argument("images", help="What image directory are labels associated with?")
parser.add_argument("-o", "--output", help="where do you want the train, val, and test directories to appear?")
# parser.add_argument("-r", "--ratio", help="define the split ratio") # TODO: complete this
args = parser.parse_args() 


# Accept label and image directories from command line args
raw_label_dir = args.labels
raw_image_dir = args.images

# Check if label & image directories exist
if os.path.isdir(raw_label_dir) == False:
    print(f'{raw_label_dir} does not exist, exiting...')
    sys.exit(1)
if os.path.isdir(raw_image_dir) == False:
    print(f'{raw_image_dir} does not exist, exiting...')
    sys.exit(1)

# DEBUG:
print(f"Raw label directory: [{raw_label_dir}]")
print(f'Raw image directory: [{raw_image_dir}]')

if args.output:
    output_directory = args.output

# Check that split ratio adds to one
if ( .99 < (split_ratio['train'] + split_ratio['val'] + split_ratio ['test']) < 1.01 ):
    pass
else:
    print("Watch out!!!! your splitt ratio != 1!")
    os._exit(1) 

# Create paths to describe the dataset output folder structure
image_train_out = os.path.join(output_directory, 'images/train')
image_val_out = os.path.join(output_directory, 'images/val')
image_test_out = os.path.join(output_directory, 'images/test')
label_train_out = os.path.join(output_directory, 'labels/train')
label_val_out = os.path.join(output_directory, 'labels/val')
label_test_out = os.path.join(output_directory, 'labels/test')


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
    image_name = image_name + '.jpg'
    input_image_path = os.path.join(raw_image_dir, image_name)

    # Copy to TRAIN 
    if( i < (num_annotations * split_ratio['train']) ):
        # Label
        if os.path.exists(input_label_path):  
            shutil.copy(input_label_path, label_train_out)
        else: 
            print(f"Label name does not exist: {input_label_path}")
        # Image 
        if os.path.exists(input_image_path):
            shutil.copy(input_image_path, image_train_out)
        else: 
            print(f"Image name does not exist: {input_image_path}")

    # Copy to VALIDATE
    elif( i < (num_annotations * (split_ratio['train'] + split_ratio['val']))): 
        # Label
        if os.path.exists(input_label_path):
            shutil.copy(input_label_path, label_val_out)
        else: 
            print(f"Label name does not exist: {input_label_path}")
        # Image 
        if os.path.exists(input_image_path):
            shutil.copy(input_image_path, image_val_out)
        else: 
            print(f"Image name does not exist: {input_image_path}")

    # Copy to TEST  
    else:
        # Label
        if os.path.exists(input_label_path):
            shutil.copy(input_label_path, label_test_out)
        else: 
            print(f"Label name does not exist: {input_label_path}")
        # Image 
        if os.path.exists(input_image_path):
            shutil.copy(input_image_path, image_test_out)
        else: 
            print(f"Image name does not exist: {input_image_path}")

