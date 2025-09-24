import os
import cv2
import json

# --- Configuration ---
INPUT_VIDEO_PATH = "../input_videos/train_video_1.mp4"
SEGMENT_DATA_PATH = "../output/segments.json"
CLIPS_OUTPUT_DIR = "../output/split_videos"

def split_video_into_clips():
    """
    Reads segment data from a JSON file and splits the input video
    into individual clips for each segment.
    """
    print("Starting video splitting process...")

    # --- Load Segment Data ---
    if not os.path.exists(SEGMENT_DATA_PATH):
        print(f"Error: Segment data file not found at {SEGMENT_DATA_PATH}")
        print("Please run '4_coach_segmentation_final.py' first to generate it.")
        return
    
    with open(SEGMENT_DATA_PATH, 'r') as f:
        segments = json.load(f)
    
    if not segments:
        print("Segment data is empty. No clips to create.")
        return

    # --- Open Main Video File ---
    cap = cv2.VideoCapture(INPUT_VIDEO_PATH)
    if not cap.isOpened():
        print(f"Error: Could not open video file {INPUT_VIDEO_PATH}")
        return

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Codec for .mp4 files

    # --- Create Clips ---
    os.makedirs(CLIPS_OUTPUT_DIR, exist_ok=True)
    print(f"Found {len(segments)} segments to process. Creating clips...")

    for segment in segments:
        seg_id = segment['id']
        seg_type = segment['type'].replace(" ", "_") # e.g., "Brake Van" -> "Brake_Van"
        start_frame = segment['start_frame']
        end_frame = segment['end_frame']

        clip_filename = f"{seg_id}_{seg_type}.mp4"
        clip_filepath = os.path.join(CLIPS_OUTPUT_DIR, clip_filename)
        
        print(f"  - Creating clip: {clip_filename} (Frames {start_frame}-{end_frame})")

        # Create a VideoWriter object for the new clip
        writer = cv2.VideoWriter(clip_filepath, fourcc, fps, (width, height))

        # Set the main video's position to the start of the segment
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        current_frame = start_frame
        while current_frame <= end_frame:
            success, frame = cap.read()
            if not success:
                break
            
            writer.write(frame)
            current_frame += 1
        
        writer.release()

    cap.release()
    print("\n✅ All video clips have been created successfully!")
    print(f"Check the '{CLIPS_OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    split_video_into_clips()