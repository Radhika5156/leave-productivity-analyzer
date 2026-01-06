# 📊 Leave & Productivity Analyzer

A **web-based application** that analyzes employee attendance and productivity using **Excel files**.  
The system processes attendance data to calculate working days, leaves, and assigns a **productivity grade**.

---

## 🚀 Features

- Upload Excel-based attendance files
- Automatic leave and attendance analysis
- Monthly productivity summary
- Productivity grading (A / B / C)
- Simple and clean user interface
- Excel-based data processing using Pandas

---

## 🖥️ Application Screens

### File Upload Screen
![Upload Screen](screens/upload.png)

### Result / Output Screen
![Output Screen](screens/output.png)

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- Pandas

---

## ⚙️ How to Run Locally

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

----
###Frontend

Open index.html in a browser
OR

Deploy the frontend using Netlify or any static hosting service

### Live Prediction API

🔗 https://relaxed-gumption-83969b.netlify.app

## Note

Backend (FastAPI) runs locally

Frontend is deployed on Netlify for demonstration

Frontend communicates with backend via HTTP requests

## Author

Radhika Vyas
---

