<h1 align="center">
🎓 EduVision AI
</h1>

<h3 align="center">
AI-Powered Student Performance Prediction & Academic Analytics Platform
</h3>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>

<img src="https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask"/>

<img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Database-SQLite-green?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Frontend-HTML%20CSS%20JavaScript-purple?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Charts-Chart.js-red?style=for-the-badge"/>

<img src="https://img.shields.io/badge/UI-Dark%20%2F%20Light%20Mode-cyan?style=for-the-badge"/>

</p>

---

# 📌 Project Overview

EduVision AI is a complete AI-driven academic analytics platform designed to help both **students** and **teachers** monitor, predict, and improve academic performance using Machine Learning.

The system predicts:

✅ Student Final Score  
✅ Pass / Fail Status  
✅ Academic Grade  
✅ Risk Level Detection  
✅ Personalized AI Suggestions  

It also provides:

📊 Advanced Analytics Dashboard  
📂 Bulk CSV/Excel Prediction System  
👨‍🏫 Teacher Monitoring Dashboard  
🤖 AI Academic Mentor  
📈 Model Performance Visualization  
📧 Email & Support System  
🌙 Modern Dark/Light Responsive UI  

---

# 🚀 Key Highlights

## 🎯 Student Features

- AI-based academic score prediction
- Pass / Fail detection
- Grade prediction
- Personalized academic guidance
- AI mentor suggestions based on:
  - Branch
  - Stream
  - Semester
  - Education type
- Risk analysis & performance monitoring
- Weekly study plan generation
- Academic analytics dashboard
- Profile management system

---

## 👨‍🏫 Teacher Features

### 📂 Bulk Prediction System

Teachers can upload:

- CSV Files
- Excel Files

to predict performance for hundreds of students simultaneously.

### 📊 Teacher Dashboard

- Total students analysis
- Pass percentage
- Failed student tracking
- Weakest student detection
- Academic alerts
- Performance summary

### 📈 Analytics Dashboard

Visualize:

- Grade Distribution
- Pass vs Fail Ratio
- Score Distribution
- AI Performance Metrics
- Model Comparison Charts

---

# 🤖 AI Academic Mentor

The system contains an intelligent AI mentor module that generates personalized guidance based on:

- Student branch
- Academic stream
- Attendance
- Assignment completion
- Study consistency
- Class participation
- Sleep hours
- Previous performance

Example:

### For CSE Students

- Focus on DSA problem solving
- Revise DBMS normalization
- Practice Operating System concepts
- Improve coding consistency

### For PCB Students

- Focus on Biology diagrams
- Revise Organic Chemistry reactions
- Improve Physics numericals

### For Commerce Students

- Practice Accountancy journal entries
- Improve Business Studies revision

---

# 🧠 Machine Learning Architecture

EduVision AI uses multiple Machine Learning models for different prediction tasks.

| Model | Purpose |
|------|------|
| Random Forest Regressor | Final Score Prediction |
| Logistic Regression | Pass / Fail Classification |
| Gradient Boosting Classifier | Grade Prediction |

---

# 📊 Model Performance

| Metric | Performance |
|------|------|
| Regression R² Score | 0.974 |
| Pass/Fail Accuracy | 97.67% |
| Grade Prediction Accuracy | 81.67% |
| Overall AI Accuracy | 92.25% |

---

# 📂 Input Features Used

The prediction system analyzes multiple academic and behavioral factors:

| Feature |
|------|
| Study Hours |
| Attendance |
| Previous Marks |
| Sleep Hours |
| Assignment Completion |
| Class Participation |
| Teacher Support |
| Internet Access |
| Learning Hours |
| Lab Usage |
| Project Submission |
| Exam Preparation |

---

# 📸 System Modules

## 🔹 Authentication System

- Student Login/Register
- Teacher Login/Register
- Forgot Password with OTP
- Email Verification

---

## 🔹 Student Dashboard

- Prediction form
- Personalized AI mentor
- Prediction result page
- Academic risk analysis
- Motivation & guidance

---

## 🔹 Bulk Prediction Module

- CSV Upload
- Excel Upload
- Real-time prediction generation
- Download prediction reports
- Recent upload tracking

---

## 🔹 Analytics Dashboard

Interactive charts for:

- Score distribution
- Grade distribution
- Pass vs fail analysis
- AI prediction analytics

---

## 🔹 Teacher Dashboard

- Bulk result tracking
- Weak student monitoring
- Failed student detection
- Record management

---

# 🛠️ Technologies Used

## 💻 Backend

- Python
- Flask
- SQLite
- Pandas
- NumPy

---

## 🤖 Machine Learning

- Scikit-learn
- Random Forest
- Logistic Regression
- Gradient Boosting
- StandardScaler
- Label Encoding

---

## 🎨 Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js
- Responsive UI Design

---

## 📧 Additional Integrations

- Flask-Mail
- OTP Authentication
- File Upload System
- PDF/CSV Export

---

# 🗂️ Project Structure

```bash
EduVision-AI/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
│
├── templates/
│   ├── dashboard.html
│   ├── analytics_dashboard.html
│   ├── teacher_dashboard.html
│   ├── bulk_prediction.html
│   ├── predict_result_ai.html
│   └── login.html
│
├── app.py
├── train_model.py
├── prediction.py
├── analytics.py
├── recommendation.py
├── ai_mentor.py
├── database.py
│
├── regression_model.pkl
├── pass_fail_model.pkl
├── grade_model.pkl
├── feature_columns.pkl
├── label_encoders.pkl
│
├── model_metrics.json
├── feature_importance.csv
├── students.db
│
└── README.md
