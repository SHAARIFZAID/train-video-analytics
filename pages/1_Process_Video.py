

import streamlit as st
import os
import tempfile
from utils.analysis import run_analysis

st.set_page_config(page_title="Process Video", page_icon="⚙️", layout="wide")
st.title("⚙️ Process & Analyze Video")

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'video_name' not in st.session_state:
    st.session_state.video_name = None
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None
if 'train_number' not in st.session_state:
    st.session_state.train_number = ""

with st.container(border=True):
    st.header("1. Enter Train Details")
    train_number = st.text_input("Enter 5 or 6-Digit Train Number", value=st.session_state.train_number, max_chars=6)
    
    st.header("2. Upload Your Video")
    uploaded_file = st.file_uploader(
        "Choose a train video file (.mp4, .mov, .avi)", 
        type=['mp4', 'mov', 'avi']
    )

if uploaded_file is not None and train_number:
    # Validate train number
    if not (train_number.isdigit() and len(train_number) >= 5):
        st.error("Please enter a valid 5 or 6-digit train number.")
    else:
        st.video(uploaded_file)
        
        with st.container(border=True):
            st.header("3. Start Analysis")
            st.write("Click the button below to start the coach detection process.")
            
            if st.button("Analyze Video Now", type="primary", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
                    file_bytes = uploaded_file.getvalue()
                    tmpfile.write(file_bytes)
                    video_path = tmpfile.name
                
                try:
                    progress_bar = st.progress(0, text="Starting analysis...")
                    def update_progress(progress, text):
                        progress_bar.progress(progress, text=text)

                    with st.spinner('Processing video... Please wait.'):
                        results = run_analysis(video_path, update_progress)
                    
                    # Store everything in session state
                    st.session_state.analysis_results = results
                    st.session_state.video_name = uploaded_file.name
                    st.session_state.last_uploaded_file = file_bytes
                    st.session_state.train_number = train_number

                    st.success("✅ Analysis Complete!")
                    st.info("Navigate to the 'View Results' page from the sidebar to see the details and download the final output.")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    if os.path.exists(video_path):
                        os.remove(video_path)
