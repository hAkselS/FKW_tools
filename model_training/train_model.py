'''
File:   train_od_model.py

Spec:   Once data is properly formatted, train_model can be used
        to apply transfer learning to a YOLO object dection model.

Usage:  python3 model_training/train_model.py <path/to/dataset.yaml> 
 
'''

from ultralytics import YOLO 
import argparse

###################################################################
# CONFIGURATION DEFAULTS
number_of_classes = 1
class_names = ['whistle']
###################################################################


parser = argparse.ArgumentParser()
parser.add_argument("yamlpath", help="Path to the dataset.yaml file is or will be")
# parser.add_argument("--create-yaml", help="Do you want to create a dataset.yaml file?")
args = parser.parse_args()

yaml_path = args.yamlpath                       # In this format: </home/gpu_enjoyer/datasets/FKW_OD_Spectrograms/formatted_dataset/dataset.yaml>

model = YOLO('yolo11n.pt')

# The dataset.yaml lives with the dataset
results = model.train(data=yaml_path, epochs=100, imgsz=640)

# TODO: add number of epochs as an arg 