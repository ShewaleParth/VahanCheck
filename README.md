# 🚗 VahanCheck: License Plate Detection & Faculty Lookup

**VahanCheck** is a smart AI-powered full-stack web application that performs real-time license plate detection using YOLOv5 and EasyOCR. It can identify Indian license plate numbers from uploaded or webcam images and match them with faculty information stored in a dataset.

## 🔍 Features

- 📷 Upload an image or capture via webcam.  
- 🧠 Detect vehicle license plates using YOLOv5.  
- 🔡 Extract plate text with EasyOCR.  
- 📍 Identify Indian state from license plate code.  
- 👨‍🏫 Match detected plate with faculty details (name, branch, contact).  
- ⚡ Responsive and interactive web interface.  

## 🧠 Tech Stack

| Layer         | Technology                     |
|---------------|--------------------------------|
| Frontend      | HTML, CSS, JavaScript          |
| Backend       | Python, Flask                  |
| AI/ML Models  | YOLOv5 (Object Detection)      |
| OCR Engine    | EasyOCR                        |
| Image Processing | OpenCV                      |
| Data Handling | Pandas, CSV                    |
| Deployment    | Railway.app / Localhost        |

## 🛠️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/ShewaleParth/VahanCheck.git  
cd VahanCheck

### 2. Install Dependencies

Make sure you have Python 3.8+ and pip installed.

pip install -r requirements.txt

### 3. Run the Application

python app2.py

Visit your app at:  
http://localhost:5000

## 📁 Project Structure

VahanCheck/  
├── app2.py                   # Flask backend logic  
├── Faculty_dataset.csv       # Faculty data for plate matching  
├── requirements.txt          # Python packages  
├── README.md                 # Project description  
│  
├── static/  
│   ├── indexx.html           # Frontend UI  
│   ├── uploads/              # Uploaded & cropped images  
│   └── pngtree-license-bg.jpg # Background image  
│  
└── yolov5/  
    └── runs/train/exp10/weights/best.pt  # YOLOv5 trained model

## 🧑‍🏫 Faculty Dataset Format

CSV file: Faculty_dataset.csv

Number Plate,Faculty Name,Branch,Contact  
MH12AB1234,Dr. A. Sharma,CSE,9876543210  
DL04XY5678,Prof. B. Verma,AI&DS,9123456789

> The app normalizes and matches plates automatically.

## 🌐 Deployment (Optional)

### Railway Deployment Steps:

1. Push code to GitHub.  
2. Go to https://railway.app and create a new project.  
3. Connect your GitHub repo.  
4. Set start command:

python app2.py

5. Make sure the PORT config is handled in app2.py using:

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

## ✅ TODO & Enhancements

- Add admin dashboard for managing plates  
- Add CSV export logs  
- Enable user login system  
- Option for cloud model hosting  
- Add multi-vehicle detection support  

## 👨‍💻 Author

**Parth Shewale**  
B.E. Artificial Intelligence & Data Science  
GitHub: https://github.com/ShewaleParth  

## 📄 License

This project is open-source and free to use for educational purposes.
