# # --- FINAL, SIMPLIFIED, AND CORRECTED SCRIPT ---
# import os
# import cv2
# from ultralytics import YOLO

# # --- Configuration ---
# MODELS_DIR = "../models/train_results"
# INPUT_VIDEO_PATH = "../input_videos/train_video_1.mp4"
# # You can adjust these rules
# MIN_COACH_DURATION = 20 # Min frames for a segment to be a valid coach

# def segment_and_count_final():
#     """
#     A robust method to segment the train by first finding all joint
#     locations and then defining coaches as the spaces between them.
#     """
#     print("Starting FINAL, ROBUST segmentation process...")

#     # --- Load Model and Video ---
#     model_path = os.path.join(MODELS_DIR, "weights/best.pt")
#     if not os.path.exists(model_path):
#         print(f"Error: Model not found at '{model_path}'")
#         return
    
#     model = YOLO(model_path)
#     class_names = model.names

#     cap = cv2.VideoCapture(INPUT_VIDEO_PATH)
#     if not cap.isOpened():
#         print(f"Error: Could not open video file {INPUT_VIDEO_PATH}")
#         return
    
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     # --- Step 1: Find all 'joint' locations in the entire video ---
#     print("Step 1: Scanning video to find all joint locations...")
#     joint_frames = []
#     frame_number = 0
#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             break
        
#         results = model(frame, verbose=False)
#         for r in results:
#             for c in r.boxes.cls:
#                 if class_names[int(c)] == 'joint':
#                     joint_frames.append(frame_number)
#                     break # Move to next frame once a joint is found
#         frame_number += 1
    
#     cap.release()
#     print(f"Step 1 Complete: Found {len(joint_frames)} frames containing a 'joint'.")

#     # --- Step 2: Define segments as the gaps between joints ---
#     print("\nStep 2: Defining segments based on joint locations...")
#     if not joint_frames:
#         print("No joints detected. Cannot segment the train.")
#         return

#     # Add start and end of video to create the first and last coach segments
#     segment_boundaries = [0] + joint_frames + [total_frames - 1]
    
#     raw_segments = []
#     for i in range(len(segment_boundaries) - 1):
#         start_f = segment_boundaries[i]
#         end_f = segment_boundaries[i+1]
#         raw_segments.append({'start_frame': start_f, 'end_frame': end_f})

#     # --- Step 3: Filter out short segments (noise) ---
#     print(f"\nStep 3: Filtering out segments shorter than {MIN_COACH_DURATION} frames...")
#     final_segments = []
#     for segment in raw_segments:
#         duration = segment['end_frame'] - segment['start_frame']
#         if duration >= MIN_COACH_DURATION:
#             final_segments.append(segment)
#     print(f"Step 3 Complete: {len(final_segments)} segments remain after filtering.")

#     # --- Step 4: Apply Classification Rules ---
#     print("\nStep 4: Applying train structure rules...")
#     engine_count = coach_count = brakevan_count = 0
#     if final_segments:
#         final_segments[0]['type'] = 'Engine'
#         if len(final_segments) > 1:
#             final_segments[-1]['type'] = 'Brake Van'
#         for i in range(1, len(final_segments) - 1):
#             final_segments[i]['type'] = 'Coach'
        
#         for i, segment in enumerate(final_segments):
#             segment['id'] = i + 1
#             if segment['type'] == 'Engine': engine_count += 1
#             elif segment['type'] == 'Coach': coach_count += 1
#             elif segment['type'] == 'Brake Van': brakevan_count += 1
    
#     # --- Final Report ---
#     print("\n" + "---" * 10)
#     print("✅ Final Processing Complete!")
#     print(f"Final Count -> Engines: {engine_count}, Coaches: {coach_count}, Brake Vans: {brakevan_count}")
#     print(f"Total Components: {len(final_segments)}")
#     print("---" * 10)
#     print("Final, Corrected Segment Details:")
#     for segment in final_segments:
#         print(f"  - {segment['type']} {segment['id']}: Frames {segment['start_frame']} to {segment['end_frame']}")

# if __name__ == "__main__":
#     segment_and_count_final()



# import os
# import cv2
# from ultralytics import YOLO
# import json # <--- ADD THIS LINE

# # --- Configuration ---
# MODELS_DIR = "../models/train_results"
# INPUT_VIDEO_PATH = "../input_videos/train_video_1.mp4"
# MIN_COACH_DURATION = 20 # Min frames for a segment to be a valid coach

# def segment_and_count_final():
#     """
#     A robust method to segment the train by first finding all joint
#     locations and then defining coaches as the spaces between them.
#     """
#     print("Starting FINAL, ROBUST segmentation process...")

#     # --- Load Model and Video ---
#     model_path = os.path.join(MODELS_DIR, "weights/best.pt")
#     if not os.path.exists(model_path):
#         print(f"Error: Model not found at '{model_path}'")
#         return
    
#     model = YOLO(model_path)
#     class_names = model.names

#     cap = cv2.VideoCapture(INPUT_VIDEO_PATH)
#     if not cap.isOpened():
#         print(f"Error: Could not open video file {INPUT_VIDEO_PATH}")
#         return
    
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     # --- Step 1: Find all 'joint' locations in the entire video ---
#     print("Step 1: Scanning video to find all joint locations...")
#     joint_frames = []
#     frame_number = 0
#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             break
        
#         results = model(frame, verbose=False)
#         for r in results:
#             for c in r.boxes.cls:
#                 if class_names[int(c)] == 'joint':
#                     joint_frames.append(frame_number)
#                     break 
#         frame_number += 1
    
#     cap.release()
#     print(f"Step 1 Complete: Found {len(joint_frames)} frames containing a 'joint'.")

#     # --- Step 2: Define segments as the gaps between joints ---
#     print("\nStep 2: Defining segments based on joint locations...")
#     if not joint_frames:
#         print("No joints detected. Cannot segment the train.")
#         return

#     segment_boundaries = [0] + joint_frames + [total_frames - 1]
    
#     raw_segments = []
#     for i in range(len(segment_boundaries) - 1):
#         start_f = segment_boundaries[i]
#         end_f = segment_boundaries[i+1]
#         raw_segments.append({'start_frame': start_f, 'end_frame': end_f})

#     # --- Step 3: Filter out short segments (noise) ---
#     print(f"\nStep 3: Filtering out segments shorter than {MIN_COACH_DURATION} frames...")
#     final_segments = []
#     for segment in raw_segments:
#         duration = segment['end_frame'] - segment['start_frame']
#         if duration >= MIN_COACH_DURATION:
#             final_segments.append(segment)
#     print(f"Step 3 Complete: {len(final_segments)} segments remain after filtering.")

#     # --- Step 4: Apply Classification Rules ---
#     print("\nStep 4: Applying train structure rules...")
#     engine_count = coach_count = brakevan_count = 0
#     if final_segments:
#         final_segments[0]['type'] = 'Engine'
#         if len(final_segments) > 1:
#             final_segments[-1]['type'] = 'Brake Van'
#         for i in range(1, len(final_segments) - 1):
#             final_segments[i]['type'] = 'Coach'
        
#         for i, segment in enumerate(final_segments):
#             segment['id'] = i + 1
#             if segment['type'] == 'Engine': engine_count += 1
#             elif segment['type'] == 'Coach': coach_count += 1
#             elif segment['type'] == 'Brake Van': brakevan_count += 1
    
#     # --- Final Report ---
#     print("\n" + "---" * 10)
#     print("✅ Final Processing Complete!")
#     print(f"Final Count -> Engines: {engine_count}, Coaches: {coach_count}, Brake Vans: {brakevan_count}")
#     print(f"Total Components: {len(final_segments)}")
#     print("---" * 10)
#     print("Final, Corrected Segment Details:")
#     for segment in final_segments:
#         print(f"  - {segment['type']} {segment['id']}: Frames {segment['start_frame']} to {segment['end_frame']}")
        
#     # --- Save results to a JSON file for the next script ---
#     output_json_path = os.path.join("../output", "segments.json")
#     os.makedirs("../output", exist_ok=True)
#     with open(output_json_path, 'w') as f:
#         json.dump(final_segments, f, indent=4)
#     print(f"\n✅ Segment data saved to {output_json_path}")

# if __name__ == "__main__":
#     segment_and_count_final()













import os
import cv2
from ultralytics import YOLO
import json

# --- Configuration ---
MODELS_DIR = "../models/train_results"
INPUT_VIDEO_PATH = "../input_videos/train_video_1.mp4"
MIN_COACH_DURATION = 20       # Min frames for a segment to be valid
LONG_SEGMENT_THRESHOLD = 80   # NEW: Any segment longer than this will be split in two

def segment_and_count_final():
    """
    Finds segments, splits very long ones, filters noise, and then
    classifies all train components.
    """
    print("Starting FINAL, ROBUST segmentation process with splitting logic...")

    # --- Step 1 & 2: Find all segments based on joint locations ---
    model_path = os.path.join(MODELS_DIR, "weights/best.pt")
    if not os.path.exists(model_path):
        print(f"Error: Model not found at '{model_path}'")
        return
    
    model = YOLO(model_path)
    class_names = model.names

    cap = cv2.VideoCapture(INPUT_VIDEO_PATH)
    if not cap.isOpened():
        print(f"Error: Could not open video file {INPUT_VIDEO_PATH}")
        return
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("Step 1: Scanning video to find all joint locations...")
    joint_frames = []
    frame_number = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        results = model(frame, verbose=False)
        for r in results:
            for c in r.boxes.cls:
                if class_names[int(c)] == 'joint':
                    joint_frames.append(frame_number)
                    break 
        frame_number += 1
    cap.release()

    segment_boundaries = [0] + joint_frames + [total_frames - 1]
    raw_segments = []
    for i in range(len(segment_boundaries) - 1):
        raw_segments.append({'start_frame': segment_boundaries[i], 'end_frame': segment_boundaries[i+1]})

    # --- Step 3: Filter out short segments (noise) ---
    print(f"\nStep 2: Filtering out segments shorter than {MIN_COACH_DURATION} frames...")
    filtered_segments = []
    for segment in raw_segments:
        if (segment['end_frame'] - segment['start_frame']) >= MIN_COACH_DURATION:
            filtered_segments.append(segment)
    print(f"Step 2 Complete: {len(filtered_segments)} segments remain after filtering.")

    # --- NEW Step 3.5: Split very long segments ---
    print(f"\nStep 3: Splitting any segment longer than {LONG_SEGMENT_THRESHOLD} frames...")
    processed_segments = []
    for segment in filtered_segments:
        duration = segment['end_frame'] - segment['start_frame']
        if duration > LONG_SEGMENT_THRESHOLD:
            split_point = segment['start_frame'] + duration // 2
            # First half
            processed_segments.append({'start_frame': segment['start_frame'], 'end_frame': split_point})
            # Second half
            processed_segments.append({'start_frame': split_point + 1, 'end_frame': segment['end_frame']})
            print(f"  - Split a long segment (frames {segment['start_frame']}-{segment['end_frame']}) into two.")
        else:
            processed_segments.append(segment)
    print(f"Step 3 Complete: Now have {len(processed_segments)} segments after splitting.")
    final_segments = processed_segments

    # --- Step 4: Apply Classification Rules ---
    print("\nStep 4: Applying train structure rules...")
    engine_count = coach_count = brakevan_count = 0
    if final_segments:
        # Re-apply rules to the potentially new list of segments
        final_segments[0]['type'] = 'Engine'
        # The second segment might also be an engine if the first was split
        if len(final_segments) > 1 and final_segments[0]['end_frame'] + 1 == final_segments[1]['start_frame']:
             final_segments[1]['type'] = 'Engine'

        if len(final_segments) > 1:
            final_segments[-1]['type'] = 'Brake Van'
        
        # Classify everything else as 'Coach'
        for i in range(len(final_segments)):
            if 'type' not in final_segments[i]:
                 final_segments[i]['type'] = 'Coach'

        # Assign IDs and count
        for i, segment in enumerate(final_segments):
            segment['id'] = i + 1
            if segment['type'] == 'Engine': engine_count += 1
            elif segment['type'] == 'Coach': coach_count += 1
            elif segment['type'] == 'Brake Van': brakevan_count += 1

    # --- Final Report ---
    print("\n" + "---" * 10)
    print("✅ Final Processing Complete!")
    print(f"Final Count -> Engines: {engine_count}, Coaches: {coach_count}, Brake Vans: {brakevan_count}")
    print(f"Total Components: {len(final_segments)}")
    print("---" * 10)
    print("Final, Corrected Segment Details:")
    for segment in final_segments:
        print(f"  - {segment['type']} {segment['id']}: Frames {segment['start_frame']} to {segment['end_frame']}")
        
    # --- Save results to a JSON file ---
    output_json_path = os.path.join("../output", "segments.json")
    os.makedirs("../output", exist_ok=True)
    with open(output_json_path, 'w') as f:
        json.dump(final_segments, f, indent=4)
    print(f"\n✅ Segment data saved to {output_json_path}")

if __name__ == "__main__":
    segment_and_count_final()