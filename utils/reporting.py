import os
import cv2
import io
import zipfile
from fpdf import FPDF

def generate_pdf_report(segments, video_path, video_name):
    """
    Generates a PDF report from the analysis results and returns it as bytes.
    """
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    
    # --- Summary Page ---
    pdf.cell(0, 20, 'Train Analysis Report', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    
    engine_count = sum(1 for s in segments if s['type'] == 'Engine')
    coach_count = sum(1 for s in segments if s['type'] == 'Coach')
    brakevan_count = sum(1 for s in segments if s['type'] == 'Brake Van')
    
    pdf.cell(0, 10, f"Source Video: {video_name}", ln=True)
    pdf.cell(0, 10, "Summary of Detected Components:", ln=True)
    pdf.cell(0, 8, f"- Engines: {engine_count}", ln=True)
    pdf.cell(0, 8, f"- Coaches: {coach_count}", ln=True)
    pdf.cell(0, 8, f"- Brake Vans: {brakevan_count}", ln=True)
    pdf.cell(0, 8, f"Total Components: {len(segments)}", ln=True)

    # --- Frame Extraction for Details ---
    cap = cv2.VideoCapture(video_path)
    for segment in segments:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        title = f"Details for: {segment['type']} #{segment['id']}"
        pdf.cell(0, 15, title, ln=True, align='C')
        
        start_frame = segment['start_frame']
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        success, frame = cap.read()
        if success:
            is_success, buffer = cv2.imencode(".jpg", frame)
            if is_success:
                img_stream = io.BytesIO(buffer)
                pdf.image(img_stream, x=15, w=180)

    cap.release()
    
    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')

def generate_clips_zip(segments, video_path):
    """
    Generates individual video clips and returns them as a single zip file in bytes.
    """
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for segment in segments:
            clip_filename = f"{segment['id']}_{segment['type'].replace(' ', '_')}.mp4"
            start_frame, end_frame = segment['start_frame'], segment['end_frame']
            
            # Save clip to a temporary file on disk
            temp_clip_path = f"temp_{clip_filename}"
            writer = cv2.VideoWriter(temp_clip_path, fourcc, fps, (width, height))
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            current_frame = start_frame
            while current_frame <= end_frame:
                success, frame = cap.read()
                if not success: break
                writer.write(frame)
                current_frame += 1
            writer.release()
            
            # Add the temp file to the zip and then delete it
            zip_file.write(temp_clip_path, arcname=clip_filename)
            os.remove(temp_clip_path)

    cap.release()
    zip_buffer.seek(0)
    return zip_buffer.getvalue()