import streamlit as st
import pandas as pd
import plotly.express as px
from utils.reporting import generate_pdf_report, generate_structured_zip
import os

st.set_page_config(page_title="View Results", page_icon="📊", layout="wide")
st.title("📊 Analysis Results")

if 'analysis_results' not in st.session_state or st.session_state.analysis_results is None:
    st.warning("No analysis has been run yet. Please go to the 'Process & Analyze Video' page to upload and process a video.")
    st.page_link("pages/1_Process_Video.py", label="Go to Processing Page", icon="⚙️")
else:
    results = st.session_state.analysis_results
    video_name = st.session_state.video_name
    train_number = st.session_state.train_number
    
    # Summary Metrics
    with st.container(border=True):
        st.header("📈 Results Summary")
        engine_count = sum(1 for s in results if s['type'] == 'Engine')
        coach_count = sum(1 for s in results if s['type'] == 'Coach')
        brakevan_count = sum(1 for s in results if s['type'] == 'Brake Van')
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Train Number", train_number)
        col2.metric("Engines Detected", f"{engine_count}")
        col3.metric("Coaches Detected", f"{coach_count}")
        col4.metric("Brake Vans Detected", f"{brakevan_count}")
        
    # Visualization
    with st.container(border=True):
        st.header("📊 Component Distribution Chart")
        df = pd.DataFrame(results)
        type_counts = df['type'].value_counts().reset_index()
        type_counts.columns = ['Component Type', 'Count']
        fig = px.bar(type_counts, x='Component Type', y='Count', color='Component Type', title=f"Component Count for Train #{train_number}")
        st.plotly_chart(fig, use_container_width=True)

    # Detailed Data Table
    with st.container(border=True):
        st.header("📋 Detailed Segment Data")
        st.dataframe(pd.DataFrame(results), use_container_width=True)

    # Download Section
    with st.container(border=True):
        st.header("📥 Download Outputs")
        if 'last_uploaded_file' in st.session_state and st.session_state.last_uploaded_file is not None:
            temp_video_path = "temp_video_for_download.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(st.session_state.last_uploaded_file)

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Generate a detailed PDF summary of the analysis.**")
                with st.spinner("Generating PDF Report..."):
                    pdf_bytes = generate_pdf_report(results, temp_video_path, video_name)
                st.download_button(label="Download PDF Report", data=pdf_bytes, file_name=f"report_{train_number}.pdf", mime="application/pdf", use_container_width=True)
            
            with col2:
                st.write("**Generate a .zip file with all videos and frames in structured folders.**")
                with st.spinner("Generating Structured Zip... This can take several minutes."):
                    zip_bytes = generate_structured_zip(results, temp_video_path, train_number)
                st.download_button(label="Download Structured Zip", data=zip_bytes, file_name=f"output_{train_number}.zip", mime="application/zip", use_container_width=True)
            
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
        else:
            st.warning("Could not find the uploaded video file to generate downloads. Please re-process.")
