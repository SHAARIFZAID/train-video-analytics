import os
import glob
from ultralytics import YOLO

# --- Configuration ---
# Path to the folder where training runs are saved
MODELS_DIR = "../models/train_results"
# Path to an input video you want to process
INPUT_VIDEO_PATH = "../input_videos/train_video_1.mp4" 
# Directory to save the output video
OUTPUT_DIR = "../output"


def run_inference():
    """
    Loads the best trained YOLO model and runs it on an input video,
    saving the result with bounding boxes.
    """
    print("Starting inference process...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # --- Find the best trained model ---
    # The 'best.pt' file is what we need from our training results
    model_path = os.path.join(MODELS_DIR, "weights/best.pt")
    
    if not os.path.exists(model_path):
        print(f"Error: Model not found at '{model_path}'")
        print("Please ensure the training was successful and the path is correct.")
        return

    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)
    
    # --- Run inference on the video ---
    print(f"Processing video: {INPUT_VIDEO_PATH}")
    
    # The 'save=True' argument tells YOLO to automatically save the output video
    # The output will be saved in a 'runs/detect/predict' folder by default
    results = model(
        INPUT_VIDEO_PATH, 
        stream=True, # Process video frame by frame to save memory
        save=True    # Save the output video with predictions
    )

    # Process the stream
    for result in results:
        # This loop is necessary to "consume" the generator and let the saving happen
        pass

    print("\n✅ Inference complete!")
    print(f"The output video has been saved in a new 'runs' folder in your main project directory.")


if __name__ == "__main__":
    run_inference()