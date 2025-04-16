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
# model_path = "models/fkw_whistle_classifier_1.pt"   # Update with your trained model path
model_path = 'models/yolo11n.pt' # TODO: replace with actual model
image_count = 1                                     # Set the number of images to process
###################################################################
input_dir = ''
# TODO: create condition that prints 'out of files' if all files in directory have been analyzed 

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="process images in this directory")
parser.add_argument("-o", "--output", help="choose a location for image outputs")
parser.add_argument("-c", "--count", type=int, default=1, help="choose number of images to analyze")

args = parser.parse_args() 
if (args.input_directory):
    input_dir = args.input_directory
else: 
    parser.error("Please specify input directory")

if (args.output):
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
else:
    output_dir = None 
    
if (args.count):
    count = int(args.count)
else:
    count = 1 

# DEBUG 
print(f'Input directory = [{input_dir}]')
if (output_dir):
    print(f'Output directory = [{output_dir}]')
print(f'Count = [{count}]')

# Load YOLO model
model = YOLO(model_path)

# Get list of JPEG images in directory
image_files = [f for f in os.listdir(input_dir) if f.endswith(".jpeg")]

# Iterate through images
i = 0
for image_file in image_files:
    '''
    Run inference on 'count' number of images.
    Save names into a csv, check for doubles. 
    '''
    image_path = os.path.join(input_dir, image_file) 
    print(f"Image path = [{image_path}]")
    
    if os.path.isfile(image_path):
        if (i > args.count): 
            print(f"Max file analysis count [{args.count}] reached, exiting...")
            sys.exit(0)
    
        with open('dataset_prediction/analyst_logs/inference_logs.csv', mode='a+', newline='') as inference_logs: 
        
            inference_logs.seek(0) # Move cursor to the start of the existing data
            reader = csv.reader(inference_logs)
           
           # Check to see if file has already been analyzed (path included)
            if any(len(row) > 0 and row[0] == image_path for row in reader):
                print(f"Already analyzed [{image_path}]")
                continue 
            
            # Run YOLO inference
            else:
                csv_entry = [] 
                writer = csv.writer(inference_logs)

                # Include the image name
                csv_entry.append(image_path)
                # writer.writerow([image_path])
                print(f"Logged [{image_path}] as analyzed")
                i = i + 1 # Only increment i if you have analyzed a file
                result = model(image_path, verbose=False)
            
                # Check if there are any detections
                detection_count = 0 
                for result in result:
                    detection_count = len(result.boxes)
                    csv_entry.append(detection_count) 

               
                if (detection_count >=1):
                    if (output_dir):
                        shutil.copy2(image_path, output_dir)
                        # Store whether or not the image have been copied to new directory
                        csv_entry.append('Copied')

                # Store: image path, number detections, if image was copied
                writer.writerow(csv_entry)
   
    else: 
        print(f'Image [{image_path}] not found')

  