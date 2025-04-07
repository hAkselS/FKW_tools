# TODO: add code spec 
# TODO: input and output directory should be args
import os
from ultralytics import YOLO
import shutil

# User-defined parameters
MODEL_PATH = "runs/detect/train7/weights/best.pt"  # Update with your trained model path
IMAGE_DIR = "/home/gpu_enjoyer/datasets/FKW_Spectrograms/images"  # Update with the directory containing images
DETECTION_OUTPUT_DIR = "test_outputs/whistle"
NUM_IMAGES = 1334  # Set the number of images to process

# Load YOLO model
model = YOLO(MODEL_PATH)

# Get list of JPEG images in directory
image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpeg")]
image_files = image_files[:NUM_IMAGES]  # Select the first X images

# Iterate through images
for image_file in image_files:
    image_path = os.path.join(IMAGE_DIR, image_file)
    
    # Run YOLO inference
    results = model(image_path, verbose=False)
    
    # Check if there are any detections
    for result in results:
        if len(result.boxes) > 0:  # If at least one detection exists
            print(image_file)
            shutil.copy2(image_path, DETECTION_OUTPUT_DIR)  # Use `image_path` instead of `result.path`
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

  