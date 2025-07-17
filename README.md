# 🚗 VahanCheck: License Plate Detection & Faculty Lookup

**VahanCheck** is a smart AI-powered full-stack web application that performs real-time license plate detection using YOLOv5 and EasyOCR. It can identify Indian license plate numbers from uploaded or webcam images and match them with faculty information stored in a dataset.

---

## 🔍 Features

- 📷 Upload an image or capture via webcam.
- 🧠 Detect vehicle license plates using **YOLOv5**.
- 🔡 Extract plate text with **EasyOCR**.
- 📍 Identify **Indian state** from license plate code.
- 👨‍🏫 Match detected plate with **faculty details** (name, branch, contact).
- ⚡ Responsive and interactive web interface.

---

## 🧠 Tech Stack

| Layer         | Technology                     |
|---------------|--------------------------------|
| Frontend      | HTML, CSS, JavaScript          |
| Backend       | Python, Flask                  |
| AI/ML Models  | YOLOv5 (Object Detection)       |
| OCR Engine    | EasyOCR                        |
| Image Processing | OpenCV                      |
| Data Handling | Pandas, CSV                    |
| Deployment    | Railway.app / Localhost        |

---

## 🛠️ Setup Instructions

### 🔁 Clone the Repository

```bash
git clone https://github.com/ShewaleParth/VahanCheck.git
cd VahanCheck
