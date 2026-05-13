import sqlite3
from datetime import datetime
import uuid


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_connection():

    conn = sqlite3.connect("students.db")

    conn.row_factory = sqlite3.Row

    return conn

# ============================================================
# STUDENT RECORD TABLE
# ============================================================

def create_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS records(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_uid TEXT,

        Study_Hours REAL,
        Attendance REAL,
        Previous_Marks REAL,
        Sleep_Hours REAL,
        Sports_Activity REAL,

        Explanation_Quality REAL,
        Student_Interaction REAL,

        Lab_Facility REAL,
        Lab_Timing REAL,

        Assignment_Completion REAL,
        Teacher_Support REAL,
        Internet_Access REAL,
        Library_Usage REAL,
        Class_Participation REAL,
        Exam_Preparation REAL,
        Learning_Hours REAL,
        Project_Submission REAL,

        study_efficiency REAL,
        health_factor REAL,
        lab_usage REAL,

        predicted_score REAL,
        result TEXT,
        grade TEXT,

        created_at TEXT

    )

    """)

    conn.commit()

    conn.close()


# ============================================================
# RANDOM UID
# ============================================================

def generate_student_uid():

    return str(uuid.uuid4())[:8]


# ============================================================
# INSERT RECORD
# ============================================================

def insert_record(data_dict):

    conn = create_connection()

    cursor = conn.cursor()

    student_uid = generate_student_uid()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""

    INSERT INTO records(

        student_uid,

        Study_Hours,
        Attendance,
        Previous_Marks,
        Sleep_Hours,
        Sports_Activity,

        Explanation_Quality,
        Student_Interaction,

        Lab_Facility,
        Lab_Timing,

        Assignment_Completion,
        Teacher_Support,
        Internet_Access,
        Library_Usage,
        Class_Participation,
        Exam_Preparation,
        Learning_Hours,
        Project_Submission,

        study_efficiency,
        health_factor,
        lab_usage,

        predicted_score,
        result,
        grade,

        created_at

    )

    VALUES(

        ?,?,?,?,?,?,
        ?,?,
        ?,?,
        ?,?,?,?,?,?,?,?,
        ?,?,?,
        ?,?,?,?

    )

    """, (

        student_uid,

        # ====================================================
        # MAIN FEATURES
        # ====================================================

        data_dict.get("Study_Hours", 0),
        data_dict.get("Attendance", 0),
        data_dict.get("Previous_Marks", 0),
        data_dict.get("Sleep_Hours", 0),
        data_dict.get("Sports_Activity", 0),

        data_dict.get("Explanation_Quality", 0),
        data_dict.get("Student_Interaction", 0),

        data_dict.get("Lab_Facility", 0),
        data_dict.get("Lab_Timing", 0),

        data_dict.get("Assignment_Completion", 0),
        data_dict.get("Teacher_Support", 0),
        data_dict.get("Internet_Access", 0),
        data_dict.get("Library_Usage", 0),
        data_dict.get("Class_Participation", 0),
        data_dict.get("Exam_Preparation", 0),
        data_dict.get("Learning_Hours", 0),
        data_dict.get("Project_Submission", 0),

        # ====================================================
        # ENGINEERED FEATURES
        # ====================================================

        data_dict.get("study_efficiency", 0),
        data_dict.get("health_factor", 0),
        data_dict.get("lab_usage", 0),

        # ====================================================
        # PREDICTION OUTPUT
        # ====================================================

        data_dict.get("predicted_score", 0),
        data_dict.get("result", ""),
        data_dict.get("grade", ""),

        current_time

    ))

    conn.commit()

    conn.close()

# ============================================================
# DELETE RECORDS
# ============================================================

def delete_all_records():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM records")

    conn.commit()

    conn.close()


# ============================================================
# USER TABLE
# ============================================================

def create_user_table():

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        role TEXT,

        full_name TEXT,

        username TEXT UNIQUE,

        email TEXT,

        password TEXT,

        dob TEXT,

        department TEXT,

        school_name TEXT,

        phone TEXT,

        profile_image TEXT DEFAULT 'default.png',

        education_type TEXT,

        stream TEXT,

        specialization TEXT,

        board TEXT,

        branch TEXT,

        semester TEXT

    )

    """)
    
    conn.commit()

    conn.close()


# ============================================================
# CREATE USER
# ============================================================


def create_user(data):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO users(

        role,
        full_name,
        username,
        email,
        password,
        dob,
        department,
        school_name,
        phone,
        education_type,
        stream,
        specialization,
        board,
        branch,
        semester

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """, (

        data["role"],
        data["full_name"],
        data["username"],
        data["email"],
        data["password"],
        data.get("dob"),
        data.get("department"),
        data.get("school_name"),
        data.get("phone"),
        data.get("education_type"),
        data.get("stream"),
        data.get("specialization"),
        data.get("board"),
        data.get("branch"),
        data.get("semester")

    ))

    conn.commit()

    conn.close()

# ============================================================
# LOGIN CHECK
# ============================================================

def check_user(username, password):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM users

    WHERE username=? AND password=?

    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# VERIFY EMAIL
# ============================================================

def verify_email(email):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM users

    WHERE email=?

    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# UPDATE PASSWORD
# ============================================================

def update_password(contact, new_password):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE users

    SET password=?

    WHERE email=? OR phone=?

    """, (

        new_password,
        contact,
        contact

    ))

    conn.commit()

    conn.close()


# ============================================================
# UPDATE PROFILE
# ============================================================

def update_profile(data):

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE users SET

    full_name=?,
    email=?,
    phone=?,
    department=?,
    employee_id=?,
    join_date=?,
    bio=?,
    profile_image=?

    WHERE username=?

    """,(

        data["full_name"],
        data["email"],
        data["phone"],  
        data["department"],
        data["employee_id"],
        data["join_date"],
        data["bio"],
        data["profile_image"],
        data["username"]

    ))

    conn.commit()

    conn.close()


# ============================================================
# GET USER
# ============================================================

def get_user(username):

    conn = sqlite3.connect("students.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM users

    WHERE username=?

    """,(username,))

    user = cursor.fetchone()

    conn.close()

    return user


# ============================================================
# BULK PREDICTION TABLE
# ============================================================

def create_bulk_prediction_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS bulk_predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        file_name TEXT,

        uploaded_by TEXT,

        total_students INTEGER,

        total_passed INTEGER,

        total_failed INTEGER,

        created_at TEXT

    )

    """)

    conn.commit()

    conn.close()


# ============================================================
# INSERT BULK PREDICTION
# ============================================================

def insert_bulk_prediction(

    file_name,
    uploaded_by,
    total_students,
    total_passed,
    total_failed

):

    conn = create_connection()

    cursor = conn.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""

    INSERT INTO bulk_predictions(

        file_name,
        uploaded_by,
        total_students,
        total_passed,
        total_failed,
        created_at

    )

    VALUES(?,?,?,?,?,?)

    """, (

        file_name,
        uploaded_by,
        total_students,
        total_passed,
        total_failed,
        current_time

    ))

    conn.commit()

    conn.close()

# ============================================================
# GET BULK PREDICTIONS
# ============================================================

def get_bulk_predictions():

    conn = create_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM bulk_predictions

    ORDER BY created_at DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data

# ============================================================
# DELETE BULK PREDICTION
# ============================================================

def delete_bulk_prediction(record_id):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM bulk_predictions

    WHERE id=?

    """,(record_id,))

    conn.commit()

    conn.close()
    
# ============================================================
# SUPPORT TABLE
# ============================================================

def create_support_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS support_messages(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_username TEXT,

        message TEXT,

        type TEXT,

        status TEXT DEFAULT 'Unread',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


# ============================================================
# INSERT SUPPORT MESSAGE
# ============================================================

def insert_support_message(username, message, msg_type):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO support_messages(

        student_username,
        message,
        type

    )

    VALUES(?,?,?)

    """,(username, message, msg_type))

    conn.commit()

    conn.close()


# ============================================================
# GET SUPPORT MESSAGES
# ============================================================
def get_support_messages():

    conn = create_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM support_messages

    ORDER BY created_at DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data

# ============================================================
# MARK MESSAGE READ
# ============================================================

def mark_support_read(message_id):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE support_messages

    SET status='Read'

    WHERE id=?

    """,(message_id,))

    conn.commit()

    conn.close()

# ============================================================
# UNREAD SUPPORT COUNT
# ============================================================

def unread_support_count():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT COUNT(*)

    FROM support_messages

    WHERE status='Unread'

    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count