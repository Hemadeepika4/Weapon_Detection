# 🔫 Weapon Detection using YOLOv12

This notebook implements a **Real-Time Weapon Detection System** using the **YOLOv12** object detection model. The system detects weapons such as knives, pistols, rifles, and other dangerous objects from images, videos, and live camera streams.

---

# 🚀 Features

- Weapon detection using YOLOv12
- Custom dataset training
- Image preprocessing
- Real-time inference
- Adaptive confidence filtering
- Threat level classification
- Evaluation metrics visualization
- Confusion matrix generation

---

# 🛠️ Technologies Used

- Python
- YOLOv12
- PyTorch
- Ultralytics
- OpenCV
- NumPy
- Matplotlib

---

# 📂 Dataset Structure

Dataset should be organized in YOLO format:

```bash
dataset/
│
├── train/
│   ├── images/
│   └── labels/
│
├── valid/
│   ├── images/
│   └── labels/
│
└── test/
    ├── images/
    └── labels/
```

---

# ⚙️ Installation

Install required libraries:

```bash
pip install ultralytics
pip install opencv-python
pip install torch torchvision
pip install numpy matplotlib
```

---

# 📘 Notebook Workflow

## 1️⃣ Import Libraries

Import required libraries such as:

- OpenCV
- NumPy
- PyTorch
- Ultralytics
- Matplotlib

---

## 2️⃣ Dataset Preparation

- Load custom dataset
- Validate labels
- Organize train/validation/test sets

---

## 3️⃣ Data Preprocessing

- Resize images to `640x640`
- Normalize pixel values
- Apply image enhancement

---

## 4️⃣ Model Training

Train YOLOv12 model using:

```python
model.train(
    data='data.yaml',
    epochs=120,
    imgsz=640,
    batch=8
)
```

---

## 5️⃣ Model Evaluation

Evaluate model performance using:

- Accuracy
- Precision
- Recall
- mAP
- Confusion Matrix

---

## 6️⃣ Image Detection

Detect weapons from input images.

Output includes:
- Bounding boxes
- Confidence scores
- Threat levels

---

## 7️⃣ Video Detection

Perform frame-by-frame weapon detection on videos.

---

## 8️⃣ Live Camera Detection

Real-time detection using webcam feed.

---

# 🎯 Adaptive Confidence Filtering

The notebook uses adaptive confidence thresholds for different weapon categories to:

- Reduce false positives
- Improve detection reliability
- Handle difficult weapon classes

---

# 🚨 Threat Levels

| Threat Level | Description |
|---|---|
| LOW | Minor threat |
| MEDIUM | Moderate threat |
| HIGH | Serious threat |
| VERY HIGH | Critical threat |

---

# 📊 Results

The notebook generates:

- Detection outputs
- Training graphs
- Loss curves
- Confusion matrix
- Precision-recall metrics

---

Dataset link:

https://www.kaggle.com/datasets/hemadeepika25/weapon-detection-custom-dataset

# ▶️ Run Notebook

Open notebook using Jupyter:

```bash
jupyter notebook
```

Then open:

```bash
weapon.ipynb
```

---

# 👨‍💻 Authors

- V. Hema Deepika
