import os
import shutil
import random
import yaml
import zipfile
from ultralytics import YOLO

# --- Configuration ---
DATASET_DIR = "../dataset"
ZIP_FILE_PATH = os.path.join(DATASET_DIR, "trainzip.zip")
# The name of the folder inside the zip file (usually 'train' or the project name)
# Check this name after you unzip it manually once to be sure.
# For this example, we assume the structure is trainzip.zip -> train/ -> images/, labels/
UNZIPPED_FOLDER_NAME = "train" 

# --- Step 1: Unzip the Dataset ---
if not os.path.exists(os.path.join(DATASET_DIR, UNZIPPED_FOLDER_NAME)):
    print(f"Unzipping {ZIP_FILE_PATH}...")
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
        zip_ref.extractall(DATASET_DIR)
    print("Unzipping complete.")
else:
    print("Dataset already unzipped.")

# --- Step 2: Automatically Create a Validation Split ---
print("Creating train/validation split...")
base_path = os.path.join(DATASET_DIR)
train_path = os.path.join(base_path, 'train')
valid_path = os.path.join(base_path, 'valid')
images_train_path = os.path.join(train_path, 'images')
labels_train_path = os.path.join(train_path, 'labels')
images_valid_path = os.path.join(valid_path, 'images')
labels_valid_path = os.path.join(valid_path, 'labels')

# Create validation directories if they don't exist
os.makedirs(images_valid_path, exist_ok=True)
os.makedirs(labels_valid_path, exist_ok=True)

# Get all image files
all_images = [f for f in os.listdir(images_train_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
random.shuffle(all_images)

# Split 20% of the data for validation
split_ratio = 0.20
split_index = int(len(all_images) * split_ratio)
valid_images = all_images[:split_index]
# The rest remain for training

# Move validation files
for img_name in valid_images:
    base_name = os.path.splitext(img_name)[0]
    label_name = f"{base_name}.txt"
    
    # Move image
    shutil.move(os.path.join(images_train_path, img_name), os.path.join(images_valid_path, img_name))
    # Move label
    shutil.move(os.path.join(labels_train_path, label_name), os.path.join(labels_valid_path, label_name))

print(f"Split complete. Moved {len(valid_images)} images to validation set.")

# --- Step 3: Find and Update the data.yaml file ---
# Roboflow usually puts the yaml inside the unzipped folder
yaml_path = os.path.join(base_path, 'data.yaml') 

if not os.path.exists(yaml_path):
    print(f"ERROR: data.yaml not found at {yaml_path}")
    print("Please check the contents of your zip file and update the path.")
else:
    print("Found data.yaml. Updating paths...")
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    # Update paths to be relative to the YAML file's location
    data['train'] = 'train/images'
    data['val'] = 'valid/images'
    
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print("data.yaml updated successfully.")

    # --- Step 4: Train the YOLO Model ---
    print("\nStarting YOLOv8 model training...")
    
    # Load a pre-trained YOLOv8 model (yolov8n.pt is small and fast)
    model = YOLO('yolov8n.pt') 
    
    # Train the model
    results = model.train(
        data=yaml_path,
        epochs=25,
        imgsz=640,
        project='../models',
        name='train_results'
    )
    print("\n✅ Training complete!")
    print("Your trained model and results are saved in the 'models/train_results' folder.")