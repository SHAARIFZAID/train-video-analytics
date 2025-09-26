# import os
# import cv2
# import io
# import zipfile
# from fpdf import FPDF

# def generate_pdf_report(segments, video_path, video_name):
#     """
#     Generates a PDF report from the analysis results and returns it as bytes.
#     """
#     pdf = FPDF('P', 'mm', 'A4')
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 24)
    
#     # --- Summary Page ---
#     pdf.cell(0, 20, 'Train Analysis Report', ln=True, align='C')
#     pdf.set_font('Arial', '', 12)
    
#     engine_count = sum(1 for s in segments if s['type'] == 'Engine')
#     coach_count = sum(1 for s in segments if s['type'] == 'Coach')
#     brakevan_count = sum(1 for s in segments if s['type'] == 'Brake Van')
    
#     pdf.cell(0, 10, f"Source Video: {video_name}", ln=True)
#     pdf.cell(0, 10, "Summary of Detected Components:", ln=True)
#     pdf.cell(0, 8, f"- Engines: {engine_count}", ln=True)
#     pdf.cell(0, 8, f"- Coaches: {coach_count}", ln=True)
#     pdf.cell(0, 8, f"- Brake Vans: {brakevan_count}", ln=True)
#     pdf.cell(0, 8, f"Total Components: {len(segments)}", ln=True)

#     # --- Frame Extraction for Details ---
#     cap = cv2.VideoCapture(video_path)
#     for segment in segments:
#         pdf.add_page()
#         pdf.set_font('Arial', 'B', 16)
#         title = f"Details for: {segment['type']} #{segment['id']}"
#         pdf.cell(0, 15, title, ln=True, align='C')
        
#         start_frame = segment['start_frame']
#         cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
#         success, frame = cap.read()
#         if success:
#             is_success, buffer = cv2.imencode(".jpg", frame)
#             if is_success:
#                 img_stream = io.BytesIO(buffer)
#                 pdf.image(img_stream, x=15, w=180)

#     cap.release()
    
#     # Return PDF as bytes
#     return pdf.output(dest='S').encode('latin-1')

# def generate_clips_zip(segments, video_path):
#     """
#     Generates individual video clips and returns them as a single zip file in bytes.
#     """
#     cap = cv2.VideoCapture(video_path)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')

#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
#         for segment in segments:
#             clip_filename = f"{segment['id']}_{segment['type'].replace(' ', '_')}.mp4"
#             start_frame, end_frame = segment['start_frame'], segment['end_frame']
            
#             # Save clip to a temporary file on disk
#             temp_clip_path = f"temp_{clip_filename}"
#             writer = cv2.VideoWriter(temp_clip_path, fourcc, fps, (width, height))
            
#             cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
#             current_frame = start_frame
#             while current_frame <= end_frame:
#                 success, frame = cap.read()
#                 if not success: break
#                 writer.write(frame)
#                 current_frame += 1
#             writer.release()
            
#             # Add the temp file to the zip and then delete it
#             zip_file.write(temp_clip_path, arcname=clip_filename)
#             os.remove(temp_clip_path)

#     cap.release()
#     zip_buffer.seek(0)
#     return zip_buffer.getvalue()












# import os
# import cv2
# import io
# import zipfile
# from fpdf import FPDF

# def generate_pdf_report(segments, video_path, video_name):
#     """
#     Generates a PDF report from the analysis results and returns it as bytes.
#     """
#     pdf = FPDF('P', 'mm', 'A4')
#     pdf.add_page()
#     pdf.set_font('Arial', 'B', 24)
    
#     # --- Summary Page ---
#     pdf.cell(0, 20, 'Train Analysis Report', ln=True, align='C')
#     pdf.set_font('Arial', '', 12)
    
#     engine_count = sum(1 for s in segments if s['type'] == 'Engine')
#     coach_count = sum(1 for s in segments if s['type'] == 'Coach')
#     brakevan_count = sum(1 for s in segments if s['type'] == 'Brake Van')
    
#     pdf.cell(0, 10, f"Source Video: {video_name}", ln=True)
#     pdf.cell(0, 10, "Summary of Detected Components:", ln=True)
#     pdf.cell(0, 8, f"- Engines: {engine_count}", ln=True)
#     pdf.cell(0, 8, f"- Coaches: {coach_count}", ln=True)
#     pdf.cell(0, 8, f"- Brake Vans: {brakevan_count}", ln=True)
#     pdf.cell(0, 8, f"Total Components: {len(segments)}", ln=True)

#     # --- Frame Extraction for Details ---
#     cap = cv2.VideoCapture(video_path)
#     for segment in segments:
#         pdf.add_page()
#         pdf.set_font('Arial', 'B', 16)
#         title = f"Details for: {segment['type']} #{segment['id']}"
#         pdf.cell(0, 15, title, ln=True, align='C')
        
#         start_frame = segment['start_frame']
#         cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
#         success, frame = cap.read()
#         if success:
#             is_success, buffer = cv2.imencode(".jpg", frame)
#             if is_success:
#                 img_stream = io.BytesIO(buffer)
#                 pdf.image(img_stream, x=15, w=180)

#     cap.release()
    
#     # --- FIXED: Explicitly convert bytearray to bytes ---
#     return bytes(pdf.output(dest='S'))

# # --- NEW FUNCTION TO GENERATE ZIP FILE ---
# def generate_clips_zip(segments, video_path):
#     """
#     Generates individual video clips and returns them as a single zip file in bytes.
#     """
#     cap = cv2.VideoCapture(video_path)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')

#     # Create a zip file in memory
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
#         for segment in segments:
#             clip_filename = f"{segment['id']}_{segment['type'].replace(' ', '_')}.mp4"
#             start_frame, end_frame = segment['start_frame'], segment['end_frame']
            
#             # Save clip to a temporary file on disk first
#             temp_clip_path = f"temp_{clip_filename}"
#             writer = cv2.VideoWriter(temp_clip_path, fourcc, fps, (width, height))
            
#             cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
#             current_frame = start_frame
#             while current_frame <= end_frame:
#                 success, frame = cap.read()
#                 if not success: break
#                 writer.write(frame)
#                 current_frame += 1
#             writer.release()
            
#             # Add the temporary file to the zip and then delete it
#             zip_file.write(temp_clip_path, arcname=clip_filename)
#             os.remove(temp_clip_path)

#     cap.release()
#     zip_buffer.seek(0) # Rewind the buffer to the beginning
#     return zip_buffer.getvalue()








import os
import cv2
import io
import zipfile
from fpdf import FPDF

def generate_pdf_report(segments, video_path, video_name):
    """
    Generates a PDF report with 4 key frames per segment.
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

    # --- Frame Extraction for Details (4 FRAMES PER SEGMENT) ---
    FRAMES_PER_COACH = 4
    cap = cv2.VideoCapture(video_path)
    for segment in segments:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        title = f"Details for: {segment['type']} #{segment['id']}"
        pdf.cell(0, 15, title, ln=True, align='C')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 5, f"(Frames {segment['start_frame']} to {segment['end_frame']})", ln=True, align='C')
        pdf.ln(5) # Add a small break

        start_frame = segment['start_frame']
        end_frame = segment['end_frame']
        duration = end_frame - start_frame

        # Loop to extract and place 4 frames in a 2x2 grid
        for i in range(FRAMES_PER_COACH):
            # Calculate evenly spaced frame positions
            if FRAMES_PER_COACH > 1:
                frame_pos = start_frame + int((i / (FRAMES_PER_COACH - 1)) * (duration - 1))
            else:
                frame_pos = start_frame
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            success, frame = cap.read()
            if success:
                is_success, buffer = cv2.imencode(".jpg", frame)
                if is_success:
                    img_stream = io.BytesIO(buffer)
                    
                    # Layout logic for a 2x2 grid
                    img_width = 85  # mm, for two images side-by-side with margin
                    x_pos = 15 if (i % 2 == 0) else 110 # X position for left/right image
                    
                    # Add a new line after the second image is placed to start the next row
                    if i == 2:
                        # Estimate image height based on a 16:9 aspect ratio to add a break
                        img_height = img_width * (9/16)
                        pdf.ln(img_height + 5) # 5mm margin

                    pdf.image(img_stream, x=x_pos, w=img_width)

    cap.release()
    
    # --- FIXED: Explicitly convert bytearray to bytes ---
    return bytes(pdf.output(dest='S'))

# --- FUNCTION TO GENERATE ZIP FILE ---
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
            
            # Save clip to a temporary file on disk first
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
            
            # Add the temporary file to the zip and then delete it
            zip_file.write(temp_clip_path, arcname=clip_filename)
            os.remove(temp_clip_path)

    cap.release()
    zip_buffer.seek(0) # Rewind the buffer to the beginning
    return zip_buffer.getvalue()

