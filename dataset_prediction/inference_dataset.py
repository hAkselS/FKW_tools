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
import csv
import sys 

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
    
if (args.count):
    count = int(args.count)

# Load YOLO model
model = YOLO(model_path)

# Get list of JPEG images in directory
image_files = [f for f in os.listdir(input_dir) if f.endswith(".jpeg")]
image_files = image_files[:image_count]  # Select the first X images

# Iterate through images

i = 0
for image_file in image_files:
    '''
    Run inference on 'count' number of images.
    Save names into a csv, check for doubles. 
    '''
    image_path = os.path.join(image_count, image_file)
    
    if os.path.isfile(image_path):
        if (i > args.count): 
            print(f"Max file analysis count [{args.count}] reached, exiting...")
            sys.exit(0)
    
        with open('dataset_prediction/analyst_logs/inference_logs.csv', mode='a+', newline='') as inference_logs: 
        
            inference_logs.seek(0) # Move cursor to the start of the existing data
            reader = csv.reader(inference_logs)
        
           
           # Check to see if file has already been analyzed
            if any(row == [image_path] for row in reader):
                print(f"Already analyzed [{image_path}]")
                continue 
            
            # Run YOLO inference
            else:
                writer = csv.writer(inference_logs)
                writer.writerow([image_path])
                print(f"Logged [{image_path}] as analyzed")
                i = i + 1 # Only increment i if you have analyzed a file
                results = model(image_path, verbose=False)
            
                # Check if there are any detections
                for result in results:
                    if len(result.boxes) > 0:  # If at least one detection exists
                        print(image_file)
                        # shutil.copy2(image_path, output_dir)  # Use `image_path` instead of `result.path`
                        break  # No need to check further boxes for this image

                            # TODO: add a True into the row associated with the image
  