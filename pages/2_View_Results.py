import streamlit as st
import pandas as pd
import plotly.express as px
from utils.reporting import generate_pdf_report, generate_clips_zip # Import our reporting functions
import os

# --- Page Configuration ---
st.set_page_config(page_title="View Results", page_icon="📊", layout="wide")
st.title("📊 Analysis Results")

# --- Check if results exist in session state ---
if 'analysis_results' not in st.session_state or st.session_state.analysis_results is None:
    st.warning("No analysis has been run yet. Please go to the 'Process & Analyze Video' page to upload and process a video.")
    # Create a link back to the processing page
    st.page_link("pages/1_Process_Video.py", label="Go to Processing Page", icon="⚙️")
else:
    # Retrieve data from session state
    results = st.session_state.analysis_results
    video_name = st.session_state.video_name
    
    # --- Summary Metrics ---
    with st.container(border=True):
        st.header("📈 Results Summary")
        engine_count = sum(1 for s in results if s['type'] == 'Engine')
        coach_count = sum(1 for s in results if s['type'] == 'Coach')
        brakevan_count = sum(1 for s in results if s['type'] == 'Brake Van')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Engines Detected", f"{engine_count} units")
        col2.metric("Coaches Detected", f"{coach_count} units")
        col3.metric("Brake Vans Detected", f"{brakevan_count} units")
        
    # --- Visualization ---
    with st.container(border=True):
        st.header("📊 Component Distribution Chart")
        df = pd.DataFrame(results)
        # Count occurrences of each component type
        type_counts = df['type'].value_counts().reset_index()
        type_counts.columns = ['Component Type', 'Count']
        
        fig = px.bar(type_counts, x='Component Type', y='Count', color='Component Type',
                     title=f"Component Count for Video: {video_name}",
                     labels={'Count': 'Number of Units', 'Component Type': 'Component'})
        st.plotly_chart(fig, use_container_width=True)

    # --- Detailed Data Table ---
    with st.container(border=True):
        st.header("📋 Detailed Segment Data")
        st.dataframe(pd.DataFrame(results), use_container_width=True)

    # --- Download Section ---
    with st.container(border=True):
        st.header("📥 Download Outputs")
        
        # We need the original video file to generate the report and clips.
        # This checks if the file was saved in the session state from the previous page.
        if 'last_uploaded_file' in st.session_state and st.session_state.last_uploaded_file is not None:
            
            # Write the in-memory file to a temporary file on disk for processing
            temp_video_path = "temp_video_for_download.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(st.session_state.last_uploaded_file)

            col1, col2 = st.columns(2)
            # --- PDF Download Button ---
            with col1:
                st.write("**Generate a detailed PDF report of the analysis.**")
                with st.spinner("Generating PDF..."):
                    pdf_bytes = generate_pdf_report(results, temp_video_path, video_name)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"report_{video_name.split('.')[0]}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            # --- Video Clips ZIP Download Button ---
            with col2:
                st.write("**Generate a .zip file containing all individual coach video clips.**")
                with st.spinner("Generating video clips... This can take a while."):
                    zip_bytes = generate_clips_zip(results, temp_video_path)
                st.download_button(
                    label="Download Video Clips (.zip)",
                    data=zip_bytes,
                    file_name=f"clips_{video_name.split('.')[0]}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            
            # Clean up the temporary video file after downloads are ready
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
        else:
            st.warning("Could not find the uploaded video file to generate downloads. Please re-process on the 'Process Video' page.")
