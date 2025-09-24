import cv2
import os
import glob

# --- Configuration ---
# Define the gap between frames to extract
FRAME_EXTRACTION_GAP = 12 
# Path to the directory containing input videos
INPUT_VIDEOS_DIR = "../input_videos"
# Path to the directory where frames will be saved
OUTPUT_FRAMES_DIR = "../dataset/raw_frames"


def extract_frames():
    """
    Extracts frames from all videos in the input directory and saves them
    to the output directory, creating folders if they don't exist.
    """
    print("Starting frame extraction process...")
    
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_FRAMES_DIR, exist_ok=True)
    
    # Find all video files (.mp4, .avi, etc.) in the input directory
    video_paths = glob.glob(os.path.join(INPUT_VIDEOS_DIR, "*.*"))
    
    if not video_paths:
        print(f"Error: No video files found in '{INPUT_VIDEOS_DIR}'.")
        print("Please add your videos to that folder.")
        return

    print(f"Found {len(video_paths)} video(s) to process.")

    # Process each video file found
    for video_path in video_paths:
        video_filename = os.path.basename(video_path)
        print(f"\nProcessing video: {video_filename}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_filename}")
            continue

        frame_count = 0
        saved_frame_count = 0
        
        while cap.isOpened():
            # Read one frame from the video
            success, frame = cap.read()
            
            if not success:
                # End of video has been reached
                break
            
            # Check if this frame should be saved based on the gap
            if frame_count % FRAME_EXTRACTION_GAP == 0:
                # Construct a unique filename for the saved frame
                output_filename = f"{os.path.splitext(video_filename)[0]}_frame_{frame_count}.jpg"
                output_path = os.path.join(OUTPUT_FRAMES_DIR, output_filename)
                
                # Save the frame as a JPG image
                cv2.imwrite(output_path, frame)
                saved_frame_count += 1

            frame_count += 1
        
        # Release the video capture object
        cap.release()
        print(f"Finished processing. Saved {saved_frame_count} frames.")

    print("\n✅ All videos processed successfully!")


if __name__ == "__main__":
    extract_frames()