'''
File:   train_od_model.py

Spec:   Once data is properly formatted, train_model can be used
        to apply transfer learning to a YOLO object dection model.

Usage:  python3 train_od_model.py

. 
'''

from ultralytics import YOLO 

model = YOLO('yolo11n.pt')

# The dataset.yaml lives with the dataset
results = model.train(data='/home/gpu_enjoyer/datasets/FKW_OD_Spectrograms/formatted_dataset/dataset.yaml', epochs=100, imgsz=640)
