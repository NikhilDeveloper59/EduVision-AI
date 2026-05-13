from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
    send_file,
    url_for
)
from prediction import predict_student
from sklearn.metrics import confusion_matrix
from database import create_support_table
from database import create_connection
from ai_mentor import generate_ai_messages
import pandas as pd
create_support_table()

from database import insert_support_message
from database import get_support_messages
from database import unread_support_count

from recommendation import (
    calculate_risk,
    student_recommendations,
    generate_study_plan,
    early_warning_message
)
from database import insert_record

import sqlite3

from flask_mail import Mail, Message
from database import get_user, update_profile

import random
import io

from database import (

    create_user,
    check_user,
    verify_email,
    update_password,
    create_table,
    create_user_table,
    get_user,

    create_bulk_prediction_table,
    insert_bulk_prediction,
    get_bulk_predictions,
    delete_bulk_prediction

)

from analytics import (
    load_data,
    grade_summary,
    pass_fail_summary,
    average_score
)

app = Flask(__name__)

app.secret_key = "student_portal_secret"

import re
import os

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ============================================================
# GMAIL SMTP
# ============================================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'nraaz590@gmail.com'

app.config['MAIL_PASSWORD'] = 'ucuo wzfv cqvw zalj'

mail = Mail(app)

# ============================================================
# SEND OTP EMAIL FUNCTION
# ============================================================

def send_otp_email(email, otp):

    msg = Message(

        "OTP Verification",

        sender=app.config['MAIL_USERNAME'],

        recipients=[email]

    )

    msg.body = f"""

Hello,

Your OTP verification code is:

{otp}

This OTP is valid for 2 minutes.

Do not share this OTP with anyone.

Regards,
Student Performance System

"""

    mail.send(msg)


@app.route("/resend-otp", methods=["POST"])

def resend_otp():

    import random
    import time

    email = session.get("email")

    if not email:

        return jsonify({
            "message":"Session expired"
        })

    # NEW OTP
    otp = str(random.randint(100000,999999))

    # SAVE OTP
    session["otp"] = otp

    # SAVE EXPIRY TIME (2 MINUTES)
    session["otp_expiry"] = time.time() + 120

    # SEND MAIL
    send_otp_email(email, otp)

    return jsonify({
        "message":"New OTP sent successfully"
    })

# ============================================================
# CREATE DATABASE TABLES
# ============================================================

create_table()

create_user_table()
create_bulk_prediction_table()

# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("login.html")


# ============================================================
# REGISTER PAGE
# ============================================================

@app.route("/register")
def register():

    return render_template("register.html")


# ============================================================
# CREATE ACCOUNT
# ============================================================

@app.route("/create-account", methods=["POST"])

def create_account():

    print("ROLE =", request.form["role"])
    print("USERNAME =", request.form["username"])

    data = {

        "role": request.form["role"],

        "full_name": request.form["full_name"],

        "username": request.form["username"],

        "email": request.form["email"],

        "password": request.form["password"],

        "dob": request.form.get("dob"),

        "education_type": request.form.get("education_type"),

        "stream": request.form.get("stream"),

        "specialization": request.form.get("specialization"),

        "board": request.form.get("board"),

        "branch": request.form.get("branch"),

        "semester": request.form.get("semester"),

        "department": request.form.get("department"),

        "school_name": request.form.get("school_name"),

        "phone": request.form.get("phone")

    }
    password = request.form["password"]

    username = request.form["username"]

    # =====================================
    # PASSWORD VALIDATION
    # =====================================

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    if not re.match(pattern, password):

        return render_template(

            "register.html",

            error="""
Password must contain:
• Uppercase Letter
• Lowercase Letter
• Number
• Special Symbol
• Minimum 8 Characters
"""
        )

    # =====================================
    # CHECK EXISTING USERNAME
    # =====================================

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE username=?",

        (username,)

    )

    existing_user = cursor.fetchone()

    conn.close()

    if existing_user:

        return render_template(

            "register.html",

            error="Username already exists"

        )

    # =====================================
    # CREATE USER
    # =====================================

    create_user(data)

    return redirect("/")


# ============================================================
# LOGIN
# ============================================================


@app.route("/login", methods=["POST"])
def login_user():

    role = request.form["role"].strip()

    username = request.form["username"]

    password = request.form["password"]

    user = check_user(username, password)

    # USER EXISTS
    if user:

        # DATABASE ROLE
        db_role = user["role"].strip()

        print("FORM ROLE =", role)
        print("DB ROLE =", db_role)

        # WRONG ROLE
        if db_role.lower() != role.lower():

            return render_template(

                "login.html",

                error="Wrong role selected"

            )

        # LOGIN SUCCESS
        session["user"] = username

        session["role"] = db_role

        # ROLE BASED REDIRECT
        if db_role.lower() == "teacher":

            return redirect("/teacher_home")

        else:

            return redirect("/dashboard")

    # INVALID LOGIN
    return render_template(

        "login.html",

        error="Invalid username or password"

    )
# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    # LOGIN CHECK
    if "user" not in session:

        return redirect("/")

    # ONLY STUDENT ACCESS
    if session.get("role") != "Student":

        return redirect("/teacher_home")

    # USER DATA
    user = get_user(session["user"])

    return render_template(

        "dashboard.html",

        username=session["user"],

        role=session["role"],

        user=user
    )
    

@app.route("/mark-read/<int:id>")

def mark_read(id):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE support_messages

    SET status='Read'

    WHERE id=?

    """,(id,))

    conn.commit()

    conn.close()

    return "success"

# ============================================================
# REPORT ISSUE
# ============================================================

@app.route("/report-issue", methods=["POST"])

def report_issue():

    if "user" not in session:

        return redirect("/")

    message = request.form["message"]

    insert_support_message(
        session["user"],
        message,
        "issue"
    )

    return redirect("/help_support")

# Give feedback
@app.route("/give_feedback")
def give_feedback():

    return render_template(
        "give_feedback.html"
    )

# ============================================
# SEND MESSAGE PAGE
# ============================================

@app.route("/send_message_page")

def send_message_page():

    return render_template(
        "send_message.html"
    )

# ============================================
# SEND MESSAGE
# ============================================

@app.route("/send_message", methods=["POST"])

def send_message():

    if "user" not in session:

        return redirect("/")

    subject = request.form["subject"]

    message = request.form["message"]

    attachment = request.files.get("attachment")

    username = session["user"]

    # =====================================
    # SAVE NOTIFICATION
    # =====================================

    insert_support_message(

        username,

        f"{subject} : {message}",

        "email"
    )

    # =====================================
    # SEND EMAIL
    # =====================================

    admin_email = app.config['MAIL_USERNAME']

    msg = Message(

        subject,

        sender=admin_email,

        recipients=[admin_email]
    )

    msg.body = f"""

New Support Message

From:
{username}

Subject:
{subject}

Message:
{message}

"""

    # =====================================
    # ATTACH FILE
    # =====================================

    if attachment and attachment.filename != "":

        msg.attach(

            attachment.filename,

            attachment.content_type,

            attachment.read()
        )

    mail.send(msg)

    return redirect("/dashboard")


# Feedback send
@app.route("/send-feedback", methods=["POST"])
def send_feedback():

    if "user" not in session:

        return redirect("/")

    feedback = request.form["feedback"]

    feedback_type = request.form.get(
        "feedback_type",
        "Feedback"
    )

    # ======================================
    # SAVE IN NOTIFICATION TABLE
    # ======================================

    insert_support_message(

        session["user"],

        f"[{feedback_type}] {feedback}",

        "feedback"

    )

    # ======================================
    # SEND EMAIL TO ADMIN
    # ======================================

    msg = Message(

        "New Feedback Received",

        sender=app.config['MAIL_USERNAME'],

        recipients=[app.config['MAIL_USERNAME']]

    )

    msg.body = f"""

New feedback received.

==================================

User:
{session["user"]}

Feedback:
{feedback}

==================================

"""

    mail.send(msg)

    return redirect("/dashboard")

# DELETE ROUTE

@app.route("/delete-notification/<int:id>")
def delete_notification(id):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM support_messages WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ============================================================
# SEND SUPPORT REPLY EMAIL
# ============================================================
@app.route("/send-support-reply", methods=["POST"])

def send_support_reply():

    if "user" not in session:

        return redirect("/")

    student_username = request.form["student_username"]

    print("FORM DATA:", request.form)

    print("USERNAME:", student_username)

    reply_message = request.form["reply_message"]

    # ==========================================
    # GET STUDENT
    # ==========================================

    student = get_user(student_username)

    if student is None:

        return "Student not found"

    # ==========================================
    # GET EMAIL
    # ==========================================

    student_email = student[4]

    # ==========================================
    # ADMIN INFO
    # ==========================================

    admin_name = session["user"]

    admin_email = app.config['MAIL_USERNAME']

    # ==========================================
    # EMAIL BODY
    # ==========================================

    subject = "📩 New Support Reply | Student Prediction Dashboard"

    body = f"""

Hello {student_username},

You received a support reply.

====================================

Reply:

{reply_message}

====================================

Reply By:
{admin_name}

Admin Email:
{admin_email}

Platform:
Student Performance Dashboard

"""

    # ==========================================
    # SEND EMAIL
    # ==========================================

    msg = Message(

        subject,

        sender=admin_email,

        recipients=[student_email]

    )

    msg.html = f"""

    <div style="

    font-family:Poppins,Arial;

    background:#f4f7ff;

    padding:40px;

    ">

    <div style="

    max-width:650px;

    margin:auto;

    background:white;

    border-radius:18px;

    overflow:hidden;

    box-shadow:0 10px 30px rgba(0,0,0,0.08);

    ">

    <!-- HEADER -->

    <div style="

    background:linear-gradient(135deg,#2563eb,#1e40af);

    padding:30px;

    text-align:center;

    color:white;

    ">

    <h1 style="margin:0;">
    📚 Student Prediction Dashboard
    </h1>

    <p style="margin-top:10px;font-size:15px;">
    Support Team Response
    </p>

    </div>

    <!-- BODY -->

    <div style="padding:35px;">

    <h2 style="color:#111;">
    Hello {student_username} 👋
    </h2>

    <p style="

    font-size:16px;

    color:#444;

    line-height:1.8;

    ">

    You received a new response from the support team.

    </p>

    <!-- MESSAGE BOX -->

    <div style="

    background:#f4f7ff;

    padding:25px;

    border-radius:14px;

    margin:25px 0;

    border-left:5px solid #2563eb;

    ">

    <p style="

    margin:0;

    font-size:16px;

    color:#111;

    line-height:1.8;

    white-space:pre-line;

    ">

    {reply_message}

    </p>

    </div>

    <!-- INFO -->

    <div style="

    background:#f9fafc;

    padding:18px;

    border-radius:12px;

    margin-top:20px;

    ">

    <p style="margin:6px 0;">
    <b>👨‍🏫 Replied By:</b> {admin_name}
    </p>

    <p style="margin:6px 0;">
    <b>📧 Admin Email:</b>
    {admin_email}
    </p>

    <p style="margin:6px 0;">
    <b>🕒 Time:</b>
    Support Team Notification
    </p>

    </div>

    <p style="

    margin-top:30px;

    color:#666;

    line-height:1.7;

    ">

    Please do not reply directly to this email.
    For additional help, use the support section inside the dashboard.

    </p>

    </div>

    <!-- FOOTER -->

    <div style="

    background:#0f172a;

    padding:18px;

    text-align:center;

    color:#cbd5e1;

    font-size:14px;

    ">

    ✨ Student Performance Prediction System

    </div>

    </div>

    </div>

    """

    mail.send(msg)

    return redirect("/dashboard")


# ============================================================
# PREDICT RESULT
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    # ========================================================
    # LOGIN CHECK
    # ========================================================

    if "user" not in session:

        return redirect("/")

    # ========================================================
    # DEBUG FORM VALUES
    # ========================================================

    print("\n================ FORM DATA ================")

    print(request.form)

    # ========================================================
    # GET AI PREDICTION
    # ========================================================

    result_data = predict_student(request.form)

    print("\n================ PREDICTION ================")

    print(result_data)

    # ========================================================
    # SAVE RECORD TO DATABASE
    # ========================================================

    db_data = {

        "Study_Hours":
        float(request.form.get("study_hours", 0)),

        "Attendance":
        float(request.form.get("attendance", 0)),

        "Previous_Marks":
        float(request.form.get("previous_marks", 0)),

        "Sleep_Hours":
        float(request.form.get("sleep_hours", 0)),

        "Sports_Activity":
        float(request.form.get("sports_activity", 0)),

        "Explanation_Quality":
        float(request.form.get("explanation_quality", 0)),

        "Student_Interaction":
        float(request.form.get("student_interaction", 0)),

        "Lab_Facility":
        float(request.form.get("lab_facility", 0)),

        "Lab_Timing":
        float(request.form.get("lab_timing", 0)),

        "Assignment_Completion":
        float(request.form.get("assignment_completion", 0)),

        "Teacher_Support":
        float(request.form.get("teacher_support", 0)),

        "Internet_Access":
        float(request.form.get("internet_access", 0)),

        "Library_Usage":
        float(request.form.get("library_usage", 0)),

        "Class_Participation":
        float(request.form.get("class_participation", 0)),

        "Exam_Preparation":
        float(request.form.get("exam_preparation", 0)),

        "Learning_Hours":
        float(request.form.get("learning_hours", 0)),

        "Project_Submission":
        float(request.form.get("project_submission", 0)),

        # ====================================================
        # ENGINEERED FEATURES
        # ====================================================

        "study_efficiency":

        float(request.form.get("study_hours", 0))

        *

        float(request.form.get("attendance", 0)),

        "health_factor":

        float(request.form.get("sleep_hours", 0))

        *

        float(request.form.get("sports_activity", 0)),

        "teacher_support":

        float(request.form.get("explanation_quality", 0))

        *

        float(request.form.get("student_interaction", 0)),

        "lab_usage":

        float(request.form.get("lab_facility", 0))

        *

        float(request.form.get("lab_timing", 0)),

        # ====================================================
        # PREDICTION OUTPUT
        # ====================================================

        "predicted_score":
        result_data["predicted_score"],

        "result":
        result_data["result"],

        "grade":
        result_data["grade"]

    }
    # ========================================================
    # SAVE INDIVIDUAL STUDENT RECORD
    # ========================================================

    insert_record(db_data)

    # ========================================================
    # AI MENTOR MESSAGES
    # ========================================================
    user = get_user(session["user"])

    # ========================================================
    # AI MENTOR MESSAGES
    # ========================================================

    ai_messages = generate_ai_messages(

        score=result_data["predicted_score"],

        attendance=float(
            request.form.get("attendance", 0)
        ),

        study_hours=float(
            request.form.get("study_hours", 0)
        ),

        sleep_hours=float(
            request.form.get("sleep_hours", 0)
        ),

        assignment_completion=float(
            request.form.get(
                "assignment_completion", 0
            )
        ),

        class_participation=int(
            request.form.get(
                "class_participation", 1
            )
        ),

        # =========================================
        # REAL USER DATA FROM DATABASE
        # =========================================

        education_type=user["education_type"],

        stream=user["stream"],

        branch=user["branch"],

        semester=user["semester"],

        board=user["board"],

        specialization=user["specialization"]

    )

    # ========================================================
    # USER DATA
    # ========================================================

    user = get_user(session["user"])

    # ========================================================
    # RENDER AI RESULT PAGE
    # ========================================================

    return render_template(

        "predict_result_ai.html",

        score=result_data["predicted_score"],

        result=result_data["result"],

        grade=result_data["grade"],

        risk=result_data["risk"],

        attendance=result_data["attendance"],

        previous_score=result_data["previous_score"],

        suggestions=result_data["suggestions"],

        weekly_plan=result_data["weekly_plan"],

        ai_messages=ai_messages,

        username=session["user"],

        role=session["role"],

        user=user
    )

# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

@app.route("/analytics")
def analytics_dashboard():

    # LOGIN CHECK
    if "user" not in session:

        return redirect("/")

    role = session.get("role")

    df = load_data()

    # ========================================================
    # EMPTY DATA
    # ========================================================

    if df.empty:

        return render_template(
            "analytics_dashboard.html",
            total_students=0,
            avg_score=0,
            pass_percentage=0,
            fail_percentage=0,
            grades={},
            score_ranges=[0,0,0,0,0]
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    total_students = len(df)

    avg_score = round(
        df["predicted_score"].mean(),
        2
    )

    pass_count, fail_count, total = pass_fail_summary(df)

    pass_percentage = round(
        (pass_count / total_students) * 100,
        1
    )

    fail_percentage = round(
        (fail_count / total_students) * 100,
        1
    )

    # ========================================================
    # GRADE DISTRIBUTION
    # ========================================================

    grade_counts = grade_summary(df)

    grades = {
        "A+": int(grade_counts.get("A+", 0)),
        "A": int(grade_counts.get("A", 0)),
        "B": int(grade_counts.get("B", 0)),
        "C": int(grade_counts.get("C", 0)),
        "D": int(grade_counts.get("D", 0)),
        "F": int(grade_counts.get("F", 0))
    }

    # ========================================================
    # SCORE DISTRIBUTION
    # ========================================================

    bins = [0,20,40,60,80,100]

    score_ranges = [0,0,0,0,0]

    for score in df["predicted_score"]:

        if score <= 20:
            score_ranges[0] += 1

        elif score <= 40:
            score_ranges[1] += 1

        elif score <= 60:
            score_ranges[2] += 1

        elif score <= 80:
            score_ranges[3] += 1

        else:
            score_ranges[4] += 1

    
   # ========================================================
    # ROLE BASED VIEW
    # ========================================================

    is_teacher = False

    if role == "Teacher":

        is_teacher = True

    # ========================================================
    # RENDER TEMPLATE
    # ========================================================

    return render_template(

        "analytics_dashboard.html",

        total_students=total_students,

        avg_score=avg_score,

        pass_percentage=pass_percentage,

        fail_percentage=fail_percentage,

        grades=grades,

        score_ranges=score_ranges,

        is_teacher=is_teacher
    )

# ============================================================
# PROFILE PAGE
# ============================================================

@app.route("/profile")

def profile():

    if "user" not in session:

        return redirect("/")

    user = get_user(session["user"])

    return render_template(

        "profile.html",

        user=user

    )


@app.route('/bulk_prediction')
def bulk_prediction():

    return render_template(
        'bulk_prediction.html'
    )

import pandas as pd


# ============================================================
# BULK PREDICTION API
# ============================================================

@app.route("/process_bulk_prediction", methods=["POST"])

def process_bulk_prediction():

    if "user" not in session:

        return jsonify({

            "success": False

        })

    file = request.files.get("file")

    if not file:

        return jsonify({

            "success": False,

            "message": "No file uploaded"

        })

    # ========================================================
    # READ FILE
    # ========================================================

    filename = file.filename.lower()

    try:

        if filename.endswith(".csv"):

            df = pd.read_csv(file)

        else:

            df = pd.read_excel(file)

    except:

        return jsonify({

            "success": False,

            "message": "Invalid file"

        })

    # ========================================================
    # REQUIRED FEATURES
    # ========================================================

    required_columns = [

        "Attendance_Percentage",

        "Previous_Exam_Marks",

        "Assignment_Completion",

        "Lab_Practice_Frequency",

        "Class_Participation",

        "Student_Behavior"

    ]

    # ========================================================
    # CHECK MISSING COLUMNS
    # ========================================================

    for col in required_columns:

        if col not in df.columns:

            return jsonify({

                "success": False,

                "message": f"Missing column: {col}"

            })

    # ========================================================
    # PREDICTION
    # ========================================================

    results = []

    total_students = len(df)

    total_passed = 0

    total_failed = 0

    for index, row in df.iterrows():

        form_data = {

            "attendance":
            row["Attendance_Percentage"],

            "previous_marks":
            row["Previous_Exam_Marks"],

            "assignment_completion":
            row["Assignment_Completion"],

            "lab_timing":
            row["Lab_Practice_Frequency"],

            "class_participation":
            row["Class_Participation"],

            "student_behavior":
            row["Student_Behavior"]
        }

        prediction = predict_student(form_data)

        if prediction["result"] == "PASS":

            total_passed += 1

        else:

            total_failed += 1

        results.append({

            "student":
            f"Student {index + 1}",

            "score":
            prediction["predicted_score"],

            "prediction":
            prediction["result"]
        })

    # ========================================================
    # SAVE BULK RECORD
    # ========================================================

    insert_bulk_prediction(

        file_name=file.filename,

        uploaded_by=session["user"],

        total_students=total_students,

        total_passed=total_passed,

        total_failed=total_failed
    )

    # ========================================================
    # RESPONSE
    # ========================================================

    return jsonify({

        "success": True,

        "results": results,

        "summary": {

            "total": total_students,

            "passed": total_passed,

            "failed": total_failed
        }
    })

# ============================================================
# DELETE BULK RECORD
# ============================================================

@app.route("/delete_bulk/<int:id>")

def delete_bulk(id):

    delete_bulk_prediction(id)

    return redirect("/teacher_dashboard")



@app.route("/help_support")
def help_support():

    return render_template(
        "help_support.html"
    )



# ============================================================
# EDIT PROFILE
# ============================================================

@app.route("/edit-profile")

def edit_profile():

    if "user" not in session:

        return redirect("/")

    user = get_user(session["user"])

    return render_template(

        "edit_profile.html",

        user=user

    )


@app.route("/update-profile", methods=["POST"])

def save_profile():

    if "user" not in session:

        return redirect("/")

    image = request.files["profile_image"]

    filename = "default.png"

    if image and image.filename != "":

        filename = secure_filename(image.filename)

        image.save(

            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

        )

    else:

        old_user = get_user(session["user"])

        filename = old_user[11]

    data = {

        "role": request.form["role"],

        "full_name": request.form["full_name"],

        "username": request.form["username"],

        "email": request.form["email"],

        "password": request.form["password"],

        "dob": request.form.get("dob"),

        "education_type":
        request.form.get("education_type"),

        "stream":
        request.form.get("stream"),

        "specialization":

        request.form.get("science_group")

        or

        request.form.get("commerce_focus")

        or

        request.form.get("arts_focus"),

        "board":
        request.form.get("board"),

        "branch":
        request.form.get("branch"),

        "semester":
        request.form.get("semester"),

        "department":
        request.form.get("department"),

        "school_name":
        request.form.get("school_name"),

        "phone":
        request.form.get("phone")
    }

    update_profile(data)

    return redirect("/profile")

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")

def logout():

    session.clear()

    return redirect("/")


# ============================================================
# FORGOT PASSWORD PAGE
# ============================================================

@app.route("/forgot-password")

def forgot_password():

    return render_template("forgot_password.html")


# ============================================================
# TEACHER DASHBOARD (BULK DATA ONLY)
# ============================================================

@app.route("/teacher_dashboard")

def teacher_dashboard():

    # ========================================================
    # LOGIN CHECK
    # ========================================================

    if "user" not in session:

        return redirect("/")

    # ========================================================
    # GET BULK DATA
    # ========================================================

    bulk_data = get_bulk_predictions()

    # ========================================================
    # EMPTY DATA
    # ========================================================

    if not bulk_data:

        return render_template(

            "teacher_dashboard.html",

            total_students=0,

            avg_score=0,

            pass_percentage=0,

            failed_students=[],

            weakest_students=[],

            attendance_alerts=[],

            teacher_message=
            "No bulk prediction records found.",

            bulk_data=[]
        )

    # ========================================================
    # TOTAL SUMMARY
    # ========================================================

    total_students = 0

    total_passed = 0

    total_failed = 0

    total_files = len(bulk_data)

    for row in bulk_data:

        total_students += row["total_students"]

        total_passed += row["total_passed"]

        total_failed += row["total_failed"]

    # ========================================================
    # AVERAGE SCORE ESTIMATION
    # ========================================================

    if total_students > 0:

        avg_score = round(

            (total_passed / total_students) * 100,

            2
        )

    else:

        avg_score = 0

    # ========================================================
    # PASS PERCENTAGE
    # ========================================================

    if total_students > 0:

        pass_percentage = round(

            (total_passed / total_students) * 100,

            2
        )

    else:

        pass_percentage = 0

    # ========================================================
    # FAILED FILES
    # ========================================================

    failed_students = []

    for row in bulk_data:

        if row["total_failed"] > 0:

            failed_students.append({

                "student_id":
                row["file_name"],

                "predicted_score":
                row["total_failed"],

                "grade":
                "Bulk File",

                "attendance":
                f"{row['total_passed']} Passed"
            })

    # ========================================================
    # WEAKEST FILES
    # ========================================================

    weakest_students = []

    sorted_bulk = sorted(

        bulk_data,

        key=lambda x: x["total_failed"],

        reverse=True

    )

    for row in sorted_bulk[:10]:

        weakest_students.append({

            "student_id":
            row["file_name"],

            "predicted_score":
            row["total_failed"],

            "attendance":
            f"{row['total_students']} Students"
        })

    # ========================================================
    # ATTENDANCE STYLE ALERTS
    # ========================================================

    attendance_alerts = []

    for row in bulk_data:

        fail_percent = 0

        if row["total_students"] > 0:

            fail_percent = (

                row["total_failed"]

                /

                row["total_students"]

            ) * 100

        if fail_percent >= 50:

            attendance_alerts.append({

                "student_id":
                row["file_name"],

                "attendance":
                round(fail_percent, 2),

                "predicted_score":
                row["total_failed"]
            })

    # ========================================================
    # AI MESSAGE
    # ========================================================

    if pass_percentage > 80:

        teacher_message = (

            "Bulk class performance is excellent. "
            "Continue supporting average students."

        )

    elif pass_percentage > 60:

        teacher_message = (

            "Class performance is moderate. "
            "Focus on weak student groups."

        )

    else:

        teacher_message = (

            "Many students are struggling. "
            "Additional academic support required."

        )

    # ========================================================
    # RENDER TEMPLATE
    # ========================================================

    return render_template(

        "teacher_dashboard.html",

        total_students=total_students,

        avg_score=avg_score,

        pass_percentage=pass_percentage,

        failed_students=failed_students,

        weakest_students=weakest_students,

        attendance_alerts=attendance_alerts,

        teacher_message=teacher_message,

        bulk_data=bulk_data,

        total_files=total_files,

        total_passed=total_passed,

        total_failed=total_failed,

        attendance_col="attendance"
    )

# ============================================================
# DELETE ALL RECORDS
# ============================================================

@app.route("/delete_all_records")

def delete_all_records():

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()

    # DELETE SINGLE STUDENT RECORDS

    cursor.execute("""

    DELETE FROM records

    """)

    # DELETE BULK PREDICTION RECORDS

    cursor.execute("""

    DELETE FROM bulk_predictions

    """)

    conn.commit()

    conn.close()

    return redirect(

        url_for("teacher_dashboard")

    )

# ============================================================
# FEATURE IMPORTANCE DASHBOARD
# ============================================================

@app.route("/feature_importance")
def feature_importance():

    try:

        feature_df = pd.read_csv(
            "feature_importance.csv"
        )

    except:

        feature_df = pd.DataFrame({

            "Feature":[
                "Study Hours",
                "Attendance",
                "Previous Marks",
                "Sleep Hours",
                "Teacher Support"
            ],

            "Importance":[
                0.24,
                0.18,
                0.15,
                0.11,
                0.08
            ]

        })

    # SORT

    feature_df = feature_df.sort_values(

        by="Importance",

        ascending=False

    )

    top_features = feature_df.head(10)

    # SHAP STYLE

    shap_explanations = [

        "Higher study hours strongly improve predicted performance.",

        "Students with better attendance receive higher scores.",

        "Previous academic marks significantly affect prediction.",

        "Sleep quality impacts concentration and academic outcome.",

        "Teacher support improves learning consistency."

    ]

    return render_template(

        "feature_importance.html",

        features=top_features["Feature"].tolist(),

        importances=top_features["Importance"].tolist(),

        shap_explanations=shap_explanations

    )


# ============================================================
# MODEL PERFORMANCE PAGE
# ============================================================

@app.route("/model_performance")

def model_performance():

    import json

    # ========================================================
    # LOAD METRICS JSON
    # ========================================================

    with open(
        "model_metrics.json",
        "r"
    ) as f:

        data = json.load(f)

    # ========================================================
    # METRICS
    # ========================================================

    metrics = {

        "regression_r2":

            round(
                data["Regression_R2"],
                3
            ),

        "mae":

            round(
                data["MAE"],
                2
            ),

        "mse":

            round(
                data["MSE"],
                2
            ),

        "rmse":

            round(
                data["RMSE"],
                2
            ),

        "pass_accuracy":

            round(
                data["PassFail_Accuracy"] * 100,
                2
            ),

        "pass_precision":

            round(
                data["PassFail_Precision"] * 100,
                2
            ),

        "pass_recall":

            round(
                data["PassFail_Recall"] * 100,
                2
            ),

        "pass_f1":

            round(
                data["PassFail_F1"] * 100,
                2
            ),

        "grade_accuracy":

            round(
                data["Grade_Accuracy"] * 100,
                2
            ),

        "grade_precision":

            round(
                data["Grade_Precision"] * 100,
                2
            ),

        "grade_recall":

            round(
                data["Grade_Recall"] * 100,
                2
            ),

        "grade_f1":

            round(
                data["Grade_F1"] * 100,
                2
            )

    }

    # ========================================================
    # OVERALL ACCURACY
    # ========================================================

    overall_accuracy = round(

        (

            metrics["regression_r2"] * 100 +

            metrics["pass_accuracy"] +

            metrics["grade_accuracy"]

        ) / 3,

        2

    )

    # ========================================================
    # COMPARISON CHART DATA
    # ========================================================

    comparison_chart = [

        round(
            metrics["regression_r2"] * 100,
            2
        ),

        metrics["pass_accuracy"],

        metrics["grade_accuracy"]

    ]

    # ========================================================
    # REGRESSION CHART DATA
    # ========================================================

    regression_chart = [

        {"x":40,"y":42},
        {"x":50,"y":52},
        {"x":60,"y":61},
        {"x":70,"y":72},
        {"x":80,"y":79}

    ]

    # ========================================================
    # PASS FAIL CHART
    # ========================================================

    pass_chart = [

        metrics["pass_accuracy"],

        round(
            100 - metrics["pass_accuracy"],
            2
        )

    ]

    # ========================================================
    # GRADE CHART
    # ========================================================

    # grade_chart = {
    #     "labels": ["A+","A","B","C","F"],
    #     "values": [750,144,166,136,304]
    #  }
    grade_chart = {
        "labels": list(data["Grade_Distribution"].keys()),
        "values": list(data["Grade_Distribution"].values())
    }
    
    # ========================================================
    # SEND TO HTML
    # ========================================================

    return render_template(

    "model_performance.html",

    metrics=metrics,

    overall_accuracy=overall_accuracy,

    regression_chart=regression_chart,

    pass_chart=pass_chart,

    grade_chart=grade_chart,

    comparison_chart=comparison_chart,

    confusion_matrix=confusion_matrix

)


# ============================================================
# VERIFY USER + SEND OTP
# ============================================================
@app.route("/verify-user", methods=["GET", "POST"])

def verify_user():

    import time

    # PREVENT DIRECT URL ACCESS
    if request.method == "GET":

        return redirect("/forgot-password")

    email = request.form.get("contact")

    # CHECK USER
    user = verify_email(email)

    if not user:

        return """

        <h1 style='font-family:Poppins;color:red;'>

        User Not Found ❌

        </h1>

        """

    # GENERATE OTP
    otp = str(random.randint(100000,999999))

    # SAVE SESSION
    session["email"] = email

    session["otp"] = otp

    session["otp_expiry"] = time.time() + 120

    session["reset_email"] = email

    session["reset_otp"] = otp

    # SEND EMAIL
    msg = Message(

        "Password Reset OTP",

        sender=app.config['MAIL_USERNAME'],

        recipients=[email]

    )

    msg.body = f"""

Hello,

Your OTP for password reset is:

{otp}

This OTP is valid for 2 minutes.

Do not share this OTP.

Regards,
Student Performance System

"""

    mail.send(msg)

    # REDIRECT OTP PAGE
    return redirect("/verify-otp")


# ============================================================
# OTP PAGE
# ============================================================

@app.route("/verify-otp")

def verify_otp_page():

    return render_template("verify_otp.html")


# ============================================================
# CHECK OTP
# ============================================================
@app.route("/check-otp", methods=["POST"])

def check_otp():

    import time

    entered_otp = request.form["otp"]

    saved_otp = session.get("otp")

    expiry = session.get("otp_expiry")

    # CHECK SESSION
    if not saved_otp or not expiry:

        return """

        <h1 style='color:red;font-family:Poppins'>

        Session Expired ❌

        </h1>

        """

    # CHECK OTP EXPIRY
    if time.time() > expiry:

        return """

        <h1 style='color:red;font-family:Poppins'>

        OTP Expired ❌

        </h1>

        """

    # VERIFY OTP
    if entered_otp == saved_otp:

        return redirect("/reset-password")

    # WRONG OTP
    return """

    <h1 style='color:red;font-family:Poppins'>

    Invalid OTP ❌

    </h1>

    """


# ============================================================
# RESET PASSWORD PAGE
# ============================================================

@app.route("/reset-password")

def reset_password_page():

    return render_template("reset_password.html")


# ============================================================
# UPDATE PASSWORD
# ============================================================

@app.route("/update-password", methods=["POST"])

def update_user_password():

    import re

    new_password = request.form["new_password"]

    confirm_password = request.form["confirm_password"]

    # ========================================================
    # PASSWORD MATCH CHECK
    # ========================================================

    if new_password != confirm_password:

        return render_template(

            "reset_password.html",

            error="Passwords do not match ❌"

        )

    # ========================================================
    # STRONG PASSWORD VALIDATION
    # ========================================================

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    if not re.match(pattern, new_password):

        return render_template(

            "reset_password.html",

            error="""
Password must contain:
• Uppercase Letter
• Lowercase Letter
• Number
• Special Symbol
• Minimum 8 Characters
"""
        )

    # ========================================================
    # GET EMAIL FROM SESSION
    # ========================================================

    email = session.get("reset_email")

    if not email:

        return redirect("/forgot-password")

    # ========================================================
    # UPDATE PASSWORD
    # ========================================================

    update_password(email, new_password)

    # ========================================================
    # CLEAR SESSION
    # ========================================================

    session.pop("reset_otp", None)

    session.pop("reset_email", None)

    session.pop("otp", None)

    session.pop("otp_expiry", None)

    # ========================================================
    # SUCCESS REDIRECT
    # ========================================================

    return redirect("/")


@app.route("/teacher_home")
def teacher_home():

    # LOGIN CHECK
    if "user" not in session:

        return redirect("/")

    # ONLY TEACHER ACCESS
    if session.get("role") != "Teacher":

        return redirect("/dashboard")

    # USER DATA
    user = get_user(session["user"])

    unread_count = unread_support_count()

    notifications = get_support_messages()

    return render_template(

        "teacher_home.html",

        username=session["user"],

        role=session["role"],

        user=user,

        unread_count=unread_count,

        notifications=notifications
    )

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)