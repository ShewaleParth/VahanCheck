import os
import cv2
import torch
import easyocr
import re
import base64
import logging
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Paths
UPLOAD_FOLDER = os.path.join("static", "uploads")
# UPLOAD_FOLDER = r"D:\Sem - 6 Mini Project\Project\static\uploads"
FACULTY_CSV_PATH = r"D:\VahanCheck\Faculty_dataset.csv"
MODEL_PATH = r"D:\VahanCheck\yolov5\yolov5\runs\train\exp10\weights\best.pt"
# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__, static_folder=r"D:\VahanCheck\static")

# Load YOLOv5 Model
try:
    model = torch.hub.load("ultralytics/yolov5", "custom", path=MODEL_PATH, force_reload=True)
    logging.info("YOLOv5 model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading YOLOv5 model: {e}")
    model = None

# Indian State Codes
STATE_CODES = {
    "AP": "Andhra Pradesh", "AR": "Arunachal Pradesh", "AS": "Assam", "BR": "Bihar", "CG": "Chhattisgarh",
    "GA": "Goa", "GJ": "Gujarat", "HR": "Haryana", "HP": "Himachal Pradesh", "JH": "Jharkhand",
    "KA": "Karnataka", "KL": "Kerala", "MP": "Madhya Pradesh", "MH": "Maharashtra", "MN": "Manipur",
    "ML": "Meghalaya", "MZ": "Mizoram", "NL": "Nagaland", "OD": "Odisha", "PB": "Punjab", "RJ": "Rajasthan",
    "SK": "Sikkim", "TN": "Tamil Nadu", "TS": "Telangana", "TR": "Tripura", "UP": "Uttar Pradesh",
    "UK": "Uttarakhand", "WB": "West Bengal", "DL": "Delhi", "PY": "Puducherry", "CH": "Chandigarh"
}

def validate_plate(plate_text):
    """Strict validation: AA 00 AA 0000 or AA00AA0000 format"""
    pattern = r"^([A-Z]{2})\s?(\d{2})\s?([A-Z]{1,2})\s?(\d{4})$"
    match = re.match(pattern, plate_text.replace(" ", "").upper())

    if match:
        state_code = match.group(1)
        return state_code, STATE_CODES.get(state_code, "Unknown State")

    return None, "Invalid Plate"

def detect_plate(image_path):
    """Detects license plate, extracts text, and validates"""
    if model is None:
        return "Model Not Loaded", None, "Error: Model Not Found", None

    results = model(image_path)

    for det in results.xyxy[0]:
        x_min, y_min, x_max, y_max, conf, cls = det
        image = cv2.imread(image_path)
        cropped_plate = image[int(y_min):int(y_max), int(x_min):int(x_max)]

        if cropped_plate is None or cropped_plate.shape[0] == 0 or cropped_plate.shape[1] == 0:
            logging.warning("No plate detected in the image.")
            return "No Plate Detected", None, "Unknown", None

        plate_path = os.path.join(UPLOAD_FOLDER, "detected_plate.jpg")
        cv2.imwrite(plate_path, cropped_plate)

        reader = easyocr.Reader(["en"])
        extracted_text = reader.readtext(plate_path, detail=0)

        plate_text = extracted_text[0] if extracted_text else "Unknown"
        state_code, state_name = validate_plate(plate_text)

        # Convert image to base64 for frontend display
        with open(plate_path, "rb") as img_file:
            detected_plate_b64 = base64.b64encode(img_file.read()).decode()

        return plate_text, state_code, state_name, f"data:image/jpeg;base64,{detected_plate_b64}"

    logging.warning("No plate detected by YOLO.")
    return "No Plate Detected", None, "Unknown", None

def normalize_plate(plate):
    """Normalize plate format to match dataset"""
    return plate.replace("-", "").replace(" ", "").upper()

def get_faculty_details(plate_text):
    """Searches for faculty details based on the detected plate"""
    try:
        df = pd.read_csv(FACULTY_CSV_PATH)
        
        # Normalize both extracted plate and dataset plates
        df["Normalized Plate"] = df["Number Plate"].apply(normalize_plate)
        normalized_plate_text = normalize_plate(plate_text)
        
        match = df[df["Normalized Plate"] == normalized_plate_text]
        
        if not match.empty:
            faculty_info = f"{match.iloc[0]['Faculty Name']}, {match.iloc[0]['Branch']}, {match.iloc[0]['Contact']}"
            return faculty_info
    except Exception as e:
        logging.error(f"Error reading faculty CSV: {e}")
    
    return "Faculty Not Found"


@app.route("/")
def index():
    return send_from_directory(r"D:\VahanCheck\static", "indexx.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles image upload, detection, and faculty lookup"""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    plate_text, state_code, state_name, detected_plate = detect_plate(file_path)

    faculty_info = get_faculty_details(plate_text)

    return jsonify({
        "plate_text": plate_text,
        "state": state_name,
        "faculty_info": faculty_info,
        "detected_plate": detected_plate
    })

if __name__ == "__main__":
    app.run(debug=True)
