import os
import uuid
import cv2
import subprocess
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from ultralytics import YOLO

from database import init_db, create_default_user, get_db_connection

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
MODEL_PATH = 'best.pt'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

init_db()
create_default_user()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

model = YOLO(MODEL_PATH)

weapon_rules = {
    "knife": {"lower": 0.40, "upper": 0.70, "threat": "LOW"},
    "chef knife": {"lower": 0.45, "upper": 0.75, "threat": "MEDIUM"},
    "butcher knife": {"lower": 0.50, "upper": 0.90, "threat": "VERY HIGH"},
    "revolver": {"lower": 0.55, "upper": 0.75, "threat": "HIGH"},
    "pistol": {"lower": 0.60, "upper": 0.85, "threat": "HIGH"},
    "sniper": {"lower": 0.70, "upper": 0.90, "threat": "HIGH"},
    "automatic rifle": {"lower": 0.60, "upper": 0.90, "threat": "VERY HIGH"},
    "smg": {"lower": 0.55, "upper": 0.85, "threat": "HIGH"},
    "shotgun": {"lower": 0.55, "upper": 0.85, "threat": "HIGH"},
    "handgun": {"lower": 0.55, "upper": 0.80, "threat": "HIGH"}
}

def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def normalize_class_name(class_name):
    return class_name.strip().lower().replace('_', ' ')

def get_detection_decision(class_name, conf):
    class_key = normalize_class_name(class_name)
    rule = weapon_rules.get(class_key)

    if rule:
        lower = rule["lower"]
        upper = rule["upper"]

        if conf < lower:
            return {
                "accepted": False,
                "threat": "REJECTED",
                "reason": "Below adaptive confidence threshold"
            }
        elif lower <= conf <= upper:
            return {
                "accepted": True,
                "threat": rule["threat"],
                "reason": "Accepted in adaptive threshold range"
            }
        else:
            return {
                "accepted": True,
                "threat": "VERY HIGH",
                "reason": "Above adaptive threshold"
            }

    if conf >= 0.50:
        return {
            "accepted": True,
            "threat": "MEDIUM",
            "reason": "Accepted using default threshold"
        }

    return {
        "accepted": False,
        "threat": "REJECTED",
        "reason": "Below default threshold"
    }

@app.route('/')
def home():
    return jsonify({
        "message": "Weapon Detection Flask Backend Running"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "status": "success",
        "message": "Backend API working properly"
    })

@app.route('/api/db-test')
def db_test():
    return jsonify({
        "status": "success",
        "message": "Database connected and initialized successfully"
    })

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not username or not email or not password:
            return jsonify({
                "status": "error",
                "message": "All fields are required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        existing_user = cursor.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if existing_user:
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Email already registered"
            }), 409

        hashed_password = generate_password_hash(password)

        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "User registered successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        user = cursor.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        conn.close()

        if not user:
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        if not check_password_hash(user['password'], password):
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email']
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/save-upload', methods=['POST'])
def save_upload():
    try:
        data = request.get_json()

        user_id = data.get('user_id')
        file_name = data.get('file_name', '').strip()
        file_type = data.get('file_type', '').strip()
        original_path = data.get('original_path', '').strip()
        output_path = data.get('output_path', '').strip()
        detection_result = data.get('detection_result', '').strip()

        if not user_id or not file_name or not file_type or not original_path:
            return jsonify({
                "status": "error",
                "message": "Missing required upload fields"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO uploads (user_id, file_name, file_type, original_path, output_path, detection_result)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (user_id, file_name, file_type, original_path, output_path, detection_result)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Upload history saved successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/uploads/<int:user_id>', methods=['GET'])
def get_uploads(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        uploads = cursor.execute(
            '''
            SELECT id, user_id, file_name, file_type, original_path, output_path, detection_result, created_at
            FROM uploads
            WHERE user_id = ?
            ORDER BY created_at DESC
            ''',
            (user_id,)
        ).fetchall()

        conn.close()

        upload_list = []
        for upload in uploads:
            upload_list.append({
                "id": upload["id"],
                "user_id": upload["user_id"],
                "file_name": upload["file_name"],
                "file_type": upload["file_type"],
                "original_path": upload["original_path"],
                "output_path": upload["output_path"],
                "detection_result": upload["detection_result"],
                "created_at": upload["created_at"]
            })

        return jsonify({
            "status": "success",
            "uploads": upload_list
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/outputs/<path:filename>')
def serve_output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/detect-image', methods=['POST'])
def detect_image():
    try:
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded"
            }), 400

        file = request.files['file']
        user_id = request.form.get('user_id')

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "User ID is required"
            }), 400

        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No selected file"
            }), 400

        if not allowed_image_file(file.filename):
            return jsonify({
                "status": "error",
                "message": "Only png, jpg, jpeg image files are allowed"
            }), 400

        original_filename = secure_filename(file.filename)
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{file_ext}"

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        output_name = f"detected_{unique_name}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_name)

        original_db_path = f"uploads/{unique_name}"
        output_db_path = f"outputs/{output_name}"

        file.save(upload_path)

        image = cv2.imread(upload_path)
        if image is None:
            return jsonify({
                "status": "error",
                "message": "Failed to read uploaded image"
            }), 400

        results = model(upload_path)
        result = results[0]

        accepted_detections = []
        weapon_detected = False

        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model.names[cls_id]

            decision = get_detection_decision(class_name, conf)

            if decision["accepted"]:
                weapon_detected = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                label = f"{class_name} {conf:.2f} {decision['threat']}"
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(
                    image,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

                accepted_detections.append({
                    "class_name": class_name,
                    "confidence": round(conf, 3),
                    "threat": decision["threat"],
                    "reason": decision["reason"]
                })

        cv2.imwrite(output_path, image)

        if weapon_detected:
            detection_result_text = "Weapon detected"
        else:
            detection_result_text = "No weapon detected"

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO uploads (user_id, file_name, file_type, original_path, output_path, detection_result)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                user_id,
                original_filename,
                'image',
                original_db_path,
                output_db_path,
                detection_result_text
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Image processed successfully",
            "weapon_detected": weapon_detected,
            "detections": accepted_detections,
            "original_file": f"/uploads/{unique_name}",
            "output_file": f"/outputs/{output_name}",
            "detection_result": detection_result_text
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/detect-video', methods=['POST'])
def detect_video():
    try:
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded"
            }), 400

        file = request.files['file']
        user_id = request.form.get('user_id')

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "User ID is required"
            }), 400

        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No selected file"
            }), 400

        if not allowed_video_file(file.filename):
            return jsonify({
                "status": "error",
                "message": "Only mp4, avi, mov, mkv video files are allowed"
            }), 400

        original_filename = secure_filename(file.filename)
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{file_ext}"

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        output_name = f"detected_{unique_name}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_name)
        temp_output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"temp_{unique_name}")

        original_db_path = f"uploads/{unique_name}"
        output_db_path = f"outputs/{output_name}"

        file.save(upload_path)

        cap = cv2.VideoCapture(upload_path)
        if not cap.isOpened():
            return jsonify({
                "status": "error",
                "message": "Failed to open uploaded video"
            }), 400

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 20.0

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output_path, fourcc, fps, (frame_width, frame_height))

        all_detections = []
        weapon_detected = False
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            results = model(frame)
            result = results[0]

            frame_detections = []

            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]

                decision = get_detection_decision(class_name, conf)

                if decision["accepted"]:
                    weapon_detected = True

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    label = f"{class_name} {conf:.2f} {decision['threat']}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(
                        frame,
                        label,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2
                    )

                    frame_detections.append({
                        "frame": frame_count,
                        "class_name": class_name,
                        "confidence": round(conf, 3),
                        "threat": decision["threat"],
                        "reason": decision["reason"]
                    })

            if frame_detections:
                all_detections.extend(frame_detections)

            out.write(frame)

        cap.release()
        out.release()

        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-i", temp_output_path,
            "-vcodec", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_path
        ]

        subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

        if weapon_detected:
            detection_result_text = "Weapon detected in video"
        else:
            detection_result_text = "No weapon detected in video"

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO uploads (user_id, file_name, file_type, original_path, output_path, detection_result)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                user_id,
                original_filename,
                'video',
                original_db_path,
                output_db_path,
                detection_result_text
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Video processed successfully",
            "weapon_detected": weapon_detected,
            "detections": all_detections,
            "original_file": f"/uploads/{unique_name}",
            "output_file": f"/outputs/{output_name}",
            "detection_result": detection_result_text
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)