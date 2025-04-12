'''
File:   inference_dataset.py

Spec:   Inference dataset is designed to inference images in a directory 
        and copy positive instances to a new location. 
        
Note:   Right now the program is only setup to handle one class.

Usage:  python3 dataset_prediction/inference_dataset.py <input/directory> -o <output/directory> -c <# of images>

'''

import os
from ultralytics import YOLO
import shutil
import argparse

###################################################################
# CONFIGURATION DEFAULTS
model_path = "models/fkw_whistle_classifier_1.pt"  # Update with your trained model path
image_count = 1  # Set the number of images to process
###################################################################
input_dir = ''

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="process images in this directory")
parser.add_argument("-o", "--output", help="choose a location for image outputs")
parser.add_argument("-c", "--count", type=int, default=1, help="choose number of images to analyze")

args = parser.parse_args() 

if (args.output):
    output_dir = args.output
else:
    parser.error("Please specify output directory")
    
# TODO: add count 

# Load YOLO model
model = YOLO(model_path)

# Get list of JPEG images in directory
image_files = [f for f in os.listdir(input_dir) if f.endswith(".jpeg")]
image_files = image_files[:image_count]  # Select the first X images

# Iterate through images
for image_file in image_files:
    image_path = os.path.join(image_count, image_file)
    
    # Run YOLO inference
    results = model(image_path, verbose=False)
    
    # Check if there are any detections
    for result in results:
        if len(result.boxes) > 0:  # If at least one detection exists
            print(image_file)
            shutil.copy2(image_path, output_dir)  # Use `image_path` instead of `result.path`
            break  # No need to check further boxes for this image





# # Get list of JPEG images in directory
# image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpeg")]
# image_files = image_files[:NUM_IMAGES]  # Select the first X images

# # Iterate through images
# images_list = []
# for image_file in image_files:
#     image_path = os.path.join(IMAGE_DIR, image_file)
#     images_list.append(image_path)

    
# # Run YOLO inference
# results = model(images_list, verbose=False, conf=0.25, classes=[0])
    
# for result in results: 
#     boxes = result.boxes
#     masks = result.masks
#     #probs = result.probs
#     obb = result.obb

#     # If there is a positive detection, move it to test_outputs/whistle
#     if (len(result.boxes) > 0):
#         shutil.copy(result.path, DETECTION_OUTPUT_DIR)
#         #result.show()

  