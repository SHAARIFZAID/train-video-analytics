# import streamlit as st
# import os

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Train Video Analytics",
#     page_icon="🚂",
#     layout="wide"
# )

# # --- Main App UI ---
# st.title("🚂 Train Video Analytics")
# st.write("Upload a video of a train's side view to count the coaches and generate a report.")

# # File uploader widget
# uploaded_file = st.file_uploader(
#     "Choose a video file", 
#     type=['mp4', 'mov', 'avi']
# )

# if uploaded_file is not None:
#     # Display the uploaded video
#     st.video(uploaded_file)
    
#     # "Process Video" button
#     if st.button("Process Video"):
#         # Placeholder for our main logic
#         st.info("Processing will start here...")





# import streamlit as st
# from streamlit_lottie import st_lottie
# from streamlit_mermaid import st_mermaid
# import requests
# import os

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Train Analytics Introduction",
#     page_icon="🚂",
#     layout="wide"
# )

# # --- Lottie Animation Helper Function ---
# def load_lottieurl(url: str):
#     """Fetches a Lottie animation from a URL."""
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # --- Load Assets ---
# lottie_animation_url = "https://assets5.lottiefiles.com/packages/lf20_t1ga2e1n.json"
# lottie_anim = load_lottieurl(lottie_animation_url)


# # --- HEADER SECTION ---
# with st.container():
#     col1, col2 = st.columns((3, 1))
#     with col1:
#         st.title("Welcome to the Train Video Analytics Suite 🚂")
#         st.subheader("An Automated Solution for Train Composition Analysis")
#     with col2:
#         if lottie_anim:
#             st_lottie(lottie_anim, speed=1, height=150, key="initial_animation")

# st.sidebar.success("Select a page from the navigation above.")
# st.markdown("---")

# # --- OVERVIEW SECTION ---
# with st.container(border=True):
#     st.header("📖 Project Overview")
#     st.write(
#         """
#         This application provides a state-of-the-art solution for analyzing train videos. 
#         By leveraging advanced computer vision and deep learning techniques, it automates 
#         the process of counting and segmenting train components with high precision.

#         The core of this project is a **YOLOv8 object detection model**, custom-trained to 
#         identify key parts of a train, which feeds into a robust, logic-based segmentation pipeline.
#         """
#     )

# st.write("") # Adds a little vertical space

# # --- INTERACTIVE METHODOLOGY SECTION ---
# with st.container(border=True):
#     st.header("⚙️ Our Interactive Methodology")

#     # The flowchart is defined using Mermaid's simple text-based syntax
#     st_mermaid("""
#         graph TD;
#             A[1. Frame Extraction] --> B(2. Object Detection);
#             B --> C{3. Smart Segmentation};
#             C --> D[4. Classification];
#             D --> E((5. Reporting));
#     """)

#     st.write("**Click on each step below to see a detailed explanation:**")

#     # Using expanders to create the "dialog box" effect
#     with st.expander("Step 1: Frame Extraction"):
#         st.write("The process begins by taking the source video and breaking it down into individual image frames, allowing the model to analyze the video on a frame-by-frame basis.")

#     with st.expander("Step 2: Object Detection"):
#         st.write("Our custom-trained YOLOv8 model processes each frame to accurately identify the 'joint' or coupling between coaches, which serves as a reliable separator.")

#     with st.expander("Step 3: Smart Segmentation"):
#         st.write("Instead of relying on flickering detections, the system first maps out all joint locations throughout the video. It then defines each coach as the sequence of frames between these stable joint markers, intelligently filtering out noise by removing segments that are too short.")
        
#     with st.expander("Step 4: Classification"):
#         st.write("Once segments are defined, logical rules based on train structure are applied. The first segment is always classified as the 'Engine', the last as the 'Brake Van', and everything in between as a 'Coach'.")
        
#     with st.expander("Step 5: Reporting"):
#         st.write("Finally, the validated data is used to generate a comprehensive PDF summary report and individual video clips for each detected train component.")

# st.write("") # Adds a little vertical space

# # --- IMAGE CAROUSEL SECTION ---
# with st.container(border=True):
#     st.header("🖼️ Dataset Generation & Augmentation in Roboflow")
#     st.write(
#         """
#         A high-quality dataset is the foundation of an accurate model. The following images showcase the 
#         process of annotating images and applying augmentations in Roboflow to create a robust training set.
#         """
#     )
    
#     # Place 5 screenshots named 'ss1.png', 'ss2.png', etc., in the 'assets' folder.
#     image_paths = [
#         "assets/ss1.png", "assets/ss2.png", "assets.ss3.png", "assets/ss4.png", "assets/ss5.png"
#     ]
#     captions = [
#         "1. Annotating coaches", "2. Brightness Augmentation", "3. Rotation Augmentation", 
#         "4. Noise Augmentation", "5. Finalizing Dataset"
#     ]

#     cols = st.columns(5)
#     for i, col in enumerate(cols):
#         with col:
#             if os.path.exists(image_paths[i]):
#                 st.image(image_paths[i], caption=captions[i], use_column_width=True)
#             else:
#                 st.warning(f"Missing: {image_paths[i]}")

# # --- Create empty page files to ensure navigation appears ---
# if not os.path.exists("pages"):
#     os.makedirs("pages")
# if not os.path.exists("pages/1_Process_Video.py"):
#     with open("pages/1_Process_Video.py", "w") as f:
#         f.write("import streamlit as st\n\nst.set_page_config(page_title='Process Video', page_icon='⚙️')\nst.title('Process & Analyze Video')")
# if not os.path.exists("pages/2_View_Results.py"):
#     with open("pages/2_View_Results.py", "w") as f:
#         f.write("import streamlit as st\n\nst.set_page_config(page_title='View Results', page_icon='📊')\nst.title('View Analysis Results')")









import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_mermaid import st_mermaid
from streamlit_carousel import carousel
import requests
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Train Analytics Introduction",
    page_icon="🚂",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background-color: #F0F2F6;
    }
    /* Target Streamlit's bordered container to create our custom card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #e1e4e8;
        border-radius: 15px;
        padding: 2rem 2rem 2rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    /* Custom header styling for h2 tags inside our new containers */
    div[data-testid="stVerticalBlockBorderWrapper"] h2 {
        border-bottom: 2px solid #e1e4e8;
        padding-bottom: 10px;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)


# --- Lottie Animation Helper Function ---
def load_lottieurl(url: str):
    """Fetches a Lottie animation from a URL."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Load Assets ---
lottie_animation_url = "https://assets5.lottiefiles.com/packages/lf20_t1ga2e1n.json"
lottie_anim = load_lottieurl(lottie_animation_url)


# --- HEADER SECTION ---
with st.container():
    col1, col2 = st.columns((3, 1))
    with col1:
        st.title("Welcome to the Train Video Analytics Suite 🚂")
        st.subheader("An Automated Solution for Train Composition Analysis")
    with col2:
        if lottie_anim:
            st_lottie(lottie_anim, speed=1, height=150, key="initial_animation")

st.sidebar.success("Select a page from the navigation above.")
st.markdown("---")


# --- SECTIONS ---

# --- OVERVIEW SECTION ---
with st.container(border=True):
    st.markdown("<h2>📖 Project Overview</h2>", unsafe_allow_html=True)
    st.write(
        """
        This application provides a state-of-the-art solution for analyzing train videos. 
        By leveraging advanced computer vision and deep learning techniques, it automates 
        the process of counting and segmenting train components with high precision.

        The core of this project is a **YOLOv8 object detection model**, custom-trained to 
        identify key parts of a train, which feeds into a robust, logic-based segmentation pipeline.
        """
    )

# --- ADVANCED METHODOLOGY DIAGRAM ---
with st.container(border=True):
    st.markdown("<h2>⚙️ System Architecture & Methodology</h2>", unsafe_allow_html=True)
    st.write("This diagram illustrates the complete workflow of our analytics pipeline, from video input to final reports.")
    st_mermaid("""
    graph TD
        subgraph INPUT
            direction TB
            A[Train Video]
        end

        subgraph "CORE ANALYTICS PIPELINE"
            direction TB
            B["1. Frame Extraction"] --> C["2. YOLOv8 Detection<br><i>Finds all 'joints'</i>"]
            C --> D["3. Smart Segmentation<br><i>Defines segments between joints</i>"]
            D --> E["4. Logic Filters<br><i>Merge close & remove short segments</i>"]
            E --> F["5. Classification<br><i>Engine → Coach → Brake Van</i>"]
        end

        subgraph OUTPUTS
            direction TB
            G["📊 Interactive Dashboard"]
            H["📄 PDF Report"]
            I["🎬 Split Video Clips"]
        end

        A --> B; F --> G; F --> H; F --> I
    """, height="600px")


# --- NEW INTERACTIVE CAROUSEL SECTION ---
with st.container(border=True):
    st.markdown("<h2>🖼️ Dataset Generation & Augmentation</h2>", unsafe_allow_html=True)
    
    # --- Instructions for you ---
    # Make sure you have 5 images (ss1.png, ss2.png, ...) in your 'assets' folder
    image_items = [
        dict(
            title="Step 1: Annotation",
            text="Annotating coaches and other components with precise bounding boxes in Roboflow.",
            img="assets/ss1.png"
        ),
        dict(
            title="Step 2: Brightness",
            text="Applying brightness augmentation to simulate different lighting conditions.",
            img="assets/ss2.png"
        ),
        dict(
            title="Step 3: Rotation",
            text="Applying slight rotation to handle variations in camera angle.",
            img="assets/ss3.png"
        ),
        dict(
            title="Step 4: Noise",
            text="Adding noise to the images to make the model more robust against video artifacts.",
            img="assets/ss4.png"
        ),
        dict(
            title="Step 5: Finalizing",
            text="Generating the final, augmented dataset version for training the YOLOv8 model.",
            img="assets/ss5.png"
        )
    ]
    
    # Check if images exist before creating the carousel
    # This avoids errors if you haven't added the screenshots yet
    for item in image_items:
        if not os.path.exists(item["img"]):
            st.warning(f"Image not found: {item['img']}. Please add your 5 screenshots to the 'assets' folder.")
            st.stop()
            
    carousel(items=image_items, width=1)


# --- Create empty page files to ensure navigation appears ---
if not os.path.exists("pages"):
    os.makedirs("pages")
if not os.path.exists("pages/1_Process_Video.py"):
    with open("pages/1_Process_Video.py", "w") as f:
        f.write("import streamlit as st\n\nst.set_page_config(page_title='Process Video', page_icon='⚙️')\nst.title('Process & Analyze Video')")
if not os.path.exists("pages/2_View_Results.py"):
    with open("pages/2_View_Results.py", "w") as f:
        f.write("import streamlit as st\n\nst.set_page_config(page_title='View Results', page_icon='📊')\nst.title('View Analysis Results')")