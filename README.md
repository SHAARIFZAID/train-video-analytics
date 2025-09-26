Train Video Analytics Suite 🚂
Project Overview
This is a comprehensive, end-to-end computer vision project designed to automate the analysis of train videos. The system takes a side-view video of a passing train as input and automatically counts the number of coaches, classifies them (Engine, Coach, Brake Van), and generates detailed, structured outputs.

The entire pipeline is wrapped in a user-friendly, multi-page Streamlit web application, making it a powerful tool for railway analysis and monitoring.

🚀 Live Demo
https://train-video-analytics-rhvntk5k6pwvxufbcungzc.streamlit.app/Process_Video

(You can paste the URL of your live Streamlit application here.)

✨ Key Features & USP (Unique Selling Propositions)
This project stands out due to its robust architecture and intelligent, real-world features. Our USPs are:

🏆 Fully Interactive Web Application:
This project is not just a collection of command-line scripts. It is a complete, multi-page Streamlit dashboard featuring an interactive UI, file uploads, progress bars, data visualizations, and downloadable outputs. This elevates the project from a simple script to a professional-grade tool.

🧠 Hybrid AI & Logic-Based Engine:
Instead of relying solely on a "black-box" AI model, this project implements a Hybrid Approach. It combines the power of a custom-trained YOLOv8 model with a smart, rule-based logic engine. This allows the system to programmatically correct minor model inaccuracies (like messy detections at the start/end of the video), ensuring the final output is highly accurate and reliable without costly retraining.

⚙️ End-to-End Automation & Structured Output:
The application fully automates the analysis workflow:

The user inputs a train number and uploads a video file.

The application processes the video in real-time, providing progress updates.

The user can then download a detailed PDF report and a structured ZIP file. This zip file contains the individual video clip and key image frames for each coach, organized into dedicated folders (<train_number>_<counter>) as per the assignment requirements.

🎯 Custom Business Logic Implementation:
The pipeline is designed to handle specific, real-world business rules, demonstrating an advanced understanding of the problem domain. This includes:

Automatically splitting an unusually long engine segment into two distinct engine units.

Applying custom frame selection logic for the PDF report (e.g., adding an offset for the first coach and capturing initial frames for the brake van).

💻 Technology Stack
Language: Python

Core Libraries:

AI/ML: PyTorch, Ultralytics (for YOLOv8)

Computer Vision: OpenCV

Web Framework: Streamlit

Data Handling: Pandas

Visualization: Plotly

PDF Generation: FPDF2

Deployment: Streamlit Community Cloud

Version Control: Git & GitHub

🛠️ Setup & Installation
To run this project on your local machine, please follow the steps below:

1. Clone the Repository:

git clone [Your GitHub Repository URL]
cd train-video-analytics


2. Create a Virtual Environment (Recommended):

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate


3. Install All Required Libraries:
The requirements.txt file contains all necessary dependencies. Run the following command:

pip install -r requirements.txt


▶️ How to Run the Application
Once all the libraries are installed, run the following command to start the application:

streamlit run app.py


Your web browser will automatically open with the application running.

📂 Project Structure
The project is organized into a clean, multi-page application structure:

├── app.py              # Main introduction page
├── pages/              # Contains the other app pages
│   ├── 1_Process_Video.py
│   └── 2_View_Results.py
├── utils/              # Contains all backend logic
│   ├── analysis.py     # Core video analysis function
│   └── reporting.py    # PDF and ZIP generation functions
├── assets/             # Contains static assets like images and flowcharts
├── models/             # Contains the trained YOLOv8 model
├── requirements.txt    # Lists all project dependencies
└── README.md           # This file


📝 Limitations & Assumptions
Video Size Limit: When deployed on Streamlit Community Cloud, the application has a file upload limit of 200 MB.

Video Angle: The system is optimized for and performs best with a clear, side-view video of the train.

Model Accuracy: While the model is highly accurate, its performance can be influenced by lighting conditions and video quality. The logic-based filters in the pipeline are designed to mitigate these variations.

Limited Dataset: The current model was trained on a limited number of videos. While manual augmentation was used to diversify the data, performance could be further improved by training on a larger and more varied dataset.
