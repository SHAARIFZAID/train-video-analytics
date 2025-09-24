# import os
# import cv2
# from ultralytics import YOLO

# # --- Configuration ---
# # Note: Paths are relative to the root of the project where app.py is
# MODELS_DIR = "models/train_results"
# MIN_COACH_DURATION = 20 # Min frames for a segment to be a valid coach

# def run_analysis(video_path, progress_callback):
#     """
#     The core analysis function. Takes a video path and a callback function
#     to update the Streamlit progress bar.
#     Returns a list of dictionaries, where each dictionary represents a detected segment.
#     """
#     # --- Load Model and Video ---
#     model_path = os.path.join(MODELS_DIR, "weights/best.pt")
#     if not os.path.exists(model_path):
#         raise FileNotFoundError(f"Model not found at '{model_path}'. Please ensure the model is trained and in the correct folder.")
    
#     model = YOLO(model_path)
#     class_names = model.names

#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         raise IOError(f"Could not open video file: {video_path}")
    
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     # --- Step 1: Find all 'joint' locations ---
#     joint_frames = []
#     for frame_number in range(total_frames):
#         cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
#         success, frame = cap.read()
#         if not success:
#             break
        
#         # Run detection and find joints
#         results = model(frame, verbose=False)
#         for r in results:
#             for c in r.boxes.cls:
#                 if class_names[int(c)] == 'joint':
#                     joint_frames.append(frame_number)
#                     break 
        
#         # Update progress bar via the callback
#         progress_callback(frame_number / total_frames, f"Scanning video for joints... (Frame {frame_number}/{total_frames})")
    
#     cap.release()
    
#     if not joint_frames:
#         return []

#     # --- Step 2: Define and Filter Segments ---
#     segment_boundaries = [0] + joint_frames + [total_frames - 1]
    
#     final_segments = []
#     raw_segments = []
#     for i in range(len(segment_boundaries) - 1):
#         start_f = segment_boundaries[i]
#         end_f = segment_boundaries[i+1]
#         duration = end_f - start_f
#         if duration >= MIN_COACH_DURATION:
#             raw_segments.append({'start_frame': start_f, 'end_frame': end_f})

#     # --- Step 3: Classify Segments ---
#     if raw_segments:
#         raw_segments[0]['type'] = 'Engine'
#         if len(raw_segments) > 1:
#             raw_segments[-1]['type'] = 'Brake Van'
#         for i in range(1, len(raw_segments) - 1):
#             raw_segments[i]['type'] = 'Coach'
        
#         for i, segment in enumerate(raw_segments):
#             segment['id'] = i + 1
#             final_segments.append(segment)
            
#     progress_callback(1.0, "Analysis complete!")
#     return final_segments


















import os
import cv2
from ultralytics import YOLO

# --- Configuration ---
# Paths are relative to the root of the project where app.py is
MODELS_DIR = "models/train_results"
MIN_COACH_DURATION = 20 # Min frames for a segment to be a valid coach

def run_analysis(video_path, progress_callback):
    """
    The core analysis function. Takes a video path and a function to report progress.
    Returns a list of dictionaries, where each dictionary represents a detected segment.
    """
    # --- Load Model and Video ---
    model_path = os.path.join(MODELS_DIR, "weights/best.pt")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at '{model_path}'. Please ensure the model is trained and in the correct folder.")
    
    model = YOLO(model_path)
    class_names = model.names

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Could not open video file: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # --- Step 1: Find all 'joint' locations ---
    joint_frames = []
    for frame_number in range(total_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = cap.read()
        if not success:
            break
        
        # Run detection on a single frame
        results = model(frame, verbose=False)
        for r in results:
            for c in r.boxes.cls:
                if class_names[int(c)] == 'joint':
                    joint_frames.append(frame_number)
                    break 
        
        # Report progress back to the Streamlit app
        progress_callback(frame_number / total_frames, f"Scanning for joints... (Frame {frame_number}/{total_frames})")
    
    cap.release()
    
    if not joint_frames:
        return [] # Return empty list if no joints are found

    # --- Step 2: Define and Filter Segments ---
    segment_boundaries = [0] + joint_frames + [total_frames - 1]
    
    final_segments = []
    raw_segments = []
    for i in range(len(segment_boundaries) - 1):
        start_f = segment_boundaries[i]
        end_f = segment_boundaries[i+1]
        duration = end_f - start_f
        if duration >= MIN_COACH_DURATION:
            raw_segments.append({'start_frame': start_f, 'end_frame': end_f})

    # --- Step 3: Classify Segments ---
    if raw_segments:
        raw_segments[0]['type'] = 'Engine'
        if len(raw_segments) > 1:
            raw_segments[-1]['type'] = 'Brake Van'
        for i in range(1, len(raw_segments) - 1):
            raw_segments[i]['type'] = 'Coach'
        
        for i, segment in enumerate(raw_segments):
            segment['id'] = i + 1
            final_segments.append(segment)
            
    progress_callback(1.0, "Analysis complete!")
    return final_segments