import os
import cv2
import json
from fpdf import FPDF

# --- Configuration ---
INPUT_VIDEO_PATH = "../input_videos/train_video_1.mp4"
SEGMENT_DATA_PATH = "../output/segments.json"
FRAMES_OUTPUT_DIR = "../output/report_frames"
PDF_OUTPUT_PATH = "../output/Train_Analysis_Report.pdf"
FRAMES_PER_COACH = 3 # Number of sample images to extract for the report

def create_report():
    """
    Generates a PDF report with a summary and detailed pages for each
    coach, including extracted key frames.
    """
    print("Starting final report generation...")

    # --- Load Segment Data ---
    if not os.path.exists(SEGMENT_DATA_PATH):
        print(f"Error: Segment data file not found at '{SEGMENT_DATA_PATH}'")
        return
    with open(SEGMENT_DATA_PATH, 'r') as f:
        segments = json.load(f)
    
    # --- Part 1: Extract Key Frames for the Report ---
    print(f"Step 1: Extracting {FRAMES_PER_COACH} key frames for each of the {len(segments)} segments...")
    os.makedirs(FRAMES_OUTPUT_DIR, exist_ok=True)
    cap = cv2.VideoCapture(INPUT_VIDEO_PATH)

    for segment in segments:
        seg_id = segment['id']
        seg_type = segment['type']
        start_frame = segment['start_frame']
        end_frame = segment['end_frame']
        duration = end_frame - start_frame
        
        # Calculate which frames to capture to get an even spread
        for i in range(FRAMES_PER_COACH):
            frame_pos = start_frame + int((i / (FRAMES_PER_COACH - 1)) * (duration - 1)) if FRAMES_PER_COACH > 1 else start_frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            success, frame = cap.read()
            if success:
                frame_filename = f"{seg_id}_{seg_type.replace(' ', '_')}_frame_{i+1}.jpg"
                frame_filepath = os.path.join(FRAMES_OUTPUT_DIR, frame_filename)
                cv2.imwrite(frame_filepath, frame)
                segment.setdefault('image_paths', []).append(frame_filepath)
    cap.release()
    print("Step 1 Complete.")

    # --- Part 2: Generate the PDF Document ---
    print("Step 2: Creating PDF document...")
    pdf = FPDF('P', 'mm', 'A4') # Portrait, millimeters, A4 size
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)

    # Summary Page
    pdf.cell(0, 20, 'Train Analysis Report', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    
    # Calculate counts
    engine_count = sum(1 for s in segments if s['type'] == 'Engine')
    coach_count = sum(1 for s in segments if s['type'] == 'Coach')
    brakevan_count = sum(1 for s in segments if s['type'] == 'Brake Van')
    
    pdf.cell(0, 10, f"Source Video: {os.path.basename(INPUT_VIDEO_PATH)}", ln=True)
    pdf.cell(0, 10, "Summary of Detected Components:", ln=True)
    pdf.cell(0, 10, f"- Engines: {engine_count}", ln=True)
    pdf.cell(0, 10, f"- Coaches: {coach_count}", ln=True)
    pdf.cell(0, 10, f"- Brake Vans: {brakevan_count}", ln=True)
    pdf.cell(0, 10, f"Total Components: {len(segments)}", ln=True)

    # Detailed Pages for each segment
    for segment in segments:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        title = f"Details for: {segment['type']} {segment['id']}"
        pdf.cell(0, 15, title, ln=True, align='C')
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Frame Range: {segment['start_frame']} to {segment['end_frame']}", ln=True)
        pdf.ln(10) # Add a 10mm break

        # Add images
        if 'image_paths' in segment:
            for i, img_path in enumerate(segment['image_paths']):
                # Place images with some margin
                # A4 width is 210mm, margins 10mm each side = 190mm usable
                img_width = 180 # mm
                pdf.image(img_path, x=15, w=img_width)
                pdf.ln(2) # Small break after image
        
    pdf.output(PDF_OUTPUT_PATH)
    print("Step 2 Complete.")
    print(f"\n✅ Report successfully generated at: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    create_report()