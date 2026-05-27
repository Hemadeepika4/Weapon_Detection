# 🔫 Real-Time Weapon Detection System (YOLOv12)

## 📌 Description

This project is a dynamic full-stack web application that detects weapons (guns, knives, etc.) in images and videos using a YOLOv12 deep learning model.

It includes:
- User authentication (Signup/Login)
- Image and video upload
- Weapon detection using YOLOv12
- Adaptive confidence filtering
- Threat level classification (LOW, MEDIUM, HIGH, VERY HIGH)
- Upload history storage using SQLite
- Angular frontend + Flask backend

---

## 🛠️ Technologies Used

Frontend:
- Angular (TypeScript, HTML, CSS)

Backend:
- Flask (Python)

Libraries:
- Ultralytics YOLOv12
- PyTorch
- OpenCV
- NumPy
- Matplotlib

Database:
- SQLite

---

## ⚙️ Installation & Setup

Follow these steps carefully.

---

### 1️⃣ Install Required Software

#### Node.js
Download: https://nodejs.org/
Check:
node -v
npm -v

#### Angular CLI
npm install -g @angular/cli
ng version

#### Python (3.10 or 3.11)
Download: https://www.python.org/downloads/
Check:
python --version

#### FFmpeg (Important for video)
Download: https://ffmpeg.org/download.html
Add to PATH and check:
ffmpeg -version

---

### 2️⃣ Backend Setup

Open terminal:
cd backend

Create virtual environment:
python -m venv venv

Activate:
venv\Scripts\activate

Install dependencies:
pip install flask flask-cors ultralytics opencv-python numpy matplotlib werkzeug torch torchvision torchaudio

Place trained model:
backend/best.pt

Run backend:
python app.py

Backend runs at:
http://127.0.0.1:5000

---

### 3️⃣ Frontend Setup

Open new terminal:
cd frontend

Install dependencies:
npm install
npm install zone.js

Run frontend:
ng serve

Frontend runs at:
http://localhost:4200

---

## 🚀 How to Run

1. Start backend:
cd backend
python app.py

2. Start frontend:
cd frontend
ng serve

3. Open browser:
http://localhost:4200

---

## 📊 Usage

1. Signup or Login
2. Upload image or video
3. Click Detect
4. View results (bounding boxes + threat level)
5. Check history page

---

## 🔄 Flow Pipeline

User → Upload → Preview → Detect → API Request → YOLO Processing → Response → Display Output → Save History

---

## 📖 Detailed Project Description

This project is an AI-powered web application designed to detect weapons in images and videos in real time using a deep learning model (YOLOv12). The system is built as a full-stack application integrating a modern frontend, a backend API, and a machine learning model.

The main objective of the system is to improve security by automatically identifying dangerous objects such as guns and knives and providing an immediate threat assessment.

---

## 🧠 How the System Works

The system follows a complete end-to-end pipeline:

1. The user uploads an image or video through the Angular frontend.
2. The file is sent to the Flask backend via REST API.
3. The backend processes the input using the YOLOv12 model.
4. The model detects objects and returns:
   - bounding boxes
   - class labels
   - confidence scores
5. A custom **Adaptive Confidence Filtering** module is applied.
6. Based on confidence levels, a **Threat Level** is assigned.
7. The processed output (image/video with detections) is returned to the frontend.
8. The result is displayed and stored in the database for history tracking.

---

## ⚙️ Adaptive Confidence Filtering (Key Feature)

Unlike standard object detection systems that use a single confidence threshold, this project introduces a **class-specific adaptive thresholding mechanism**.

For each weapon type:
- A lower threshold filters weak detections
- An upper threshold determines severity

### Decision Logic:
- Confidence < Lower Threshold → Rejected
- Lower ≤ Confidence ≤ Upper → Normal Threat (LOW/MEDIUM/HIGH)
- Confidence > Upper → VERY HIGH Threat

This improves:
- accuracy
- false positive reduction
- interpretability of results

---

## 🎯 Threat Level Classification

Each detection is categorized into one of the following:

- LOW
- MEDIUM
- HIGH
- VERY HIGH

This helps users quickly understand the severity of the detected object instead of only seeing raw confidence values.

---

## 🎥 Video Processing Approach

For video inputs:
- The video is split into frames using OpenCV
- Each frame is processed individually by YOLOv12
- Bounding boxes are drawn frame-by-frame
- Frames are recombined into a video
- FFmpeg is used to convert the output into a browser-compatible format (H.264)

---

## 🗄️ Database Functionality

The system uses SQLite to store:

- User details (login/signup)
- Uploaded files
- Processed outputs
- Detection results
- Timestamps

This allows:
- history tracking
- user-specific data management

---

## 🌐 Frontend Functionality

The Angular frontend provides:

- Attractive UI for better user experience
- Instant preview of uploaded files
- Dynamic result display
- History viewing page
- Secure login/logout flow

---

## 🔗 Backend Responsibilities

The Flask backend handles:

- API requests from frontend
- Model loading and inference
- Image/video processing
- Adaptive filtering logic
- Database operations
- Serving processed files

---


## 👩‍💻 Author

HEMA DEEPIKA VELAGA

Project Title:
A Real-Time Weapon Detection System with Adaptive Confidence Filtering Using YOLOv12
