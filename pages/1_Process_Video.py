import streamlit as st
import os
import tempfile
from utils.analysis import run_analysis # Import our analysis function

# --- Page Configuration ---
st.set_page_config(page_title="Process Video", page_icon="⚙️", layout="wide")
st.title("⚙️ Process & Analyze Video")

# --- Initialize session state for storing results ---
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'video_name' not in st.session_state:
    st.session_state.video_name = None
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# --- UI Elements ---
with st.container(border=True):
    st.header("1. Upload Your Video")
    uploaded_file = st.file_uploader(
        "Choose a train video file (.mp4, .mov, .avi)", 
        type=['mp4', 'mov', 'avi']
    )

if uploaded_file is not None:
    st.video(uploaded_file)
    
    with st.container(border=True):
        st.header("2. Start Analysis")
        st.write("Click the button below to start the coach detection and segmentation process. This may take several minutes depending on the video length.")
        
        if st.button("Analyze Video Now", type="primary", use_container_width=True):
            
            # Save uploaded file to a temporary file on disk
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
                # Save the file content for processing
                file_bytes = uploaded_file.getvalue()
                tmpfile.write(file_bytes)
                video_path = tmpfile.name
            
            try:
                # Create a placeholder for the progress bar
                progress_bar = st.progress(0, text="Starting analysis...")
                
                # Define a function that the analysis logic can call to update the UI
                def update_progress(progress, text):
                    progress_bar.progress(progress, text=text)

                with st.spinner('Processing video... Please wait.'):
                    results = run_analysis(video_path, update_progress)
                
                # Store results and the video file bytes in session state for other pages
                st.session_state.analysis_results = results
                st.session_state.video_name = uploaded_file.name
                st.session_state.last_uploaded_file = file_bytes # Save file bytes for later use

                st.success("✅ Analysis Complete!")
                st.info("Results are ready. Navigate to the 'View Results' page from the sidebar to see the details.")
                
            except FileNotFoundError as e:
                st.error(f"Error: {e}. Please make sure the 'models' folder is in your project directory.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
            finally:
                # Clean up the temporary file from disk
                if os.path.exists(video_path):
                    os.remove(video_path)