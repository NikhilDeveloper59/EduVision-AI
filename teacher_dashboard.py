"""
teacher_dashboard.py
-----------------------------------------
Teacher Support Module
Updated for New Student Dataset
"""

import pandas as pd


# ============================================================
# 1️⃣ CLASS SUMMARY
# ============================================================

def class_summary(df):

    if df.empty:

        return {

            "total_students": 0,
            "avg_score": 0,
            "pass_percent": 0

        }

    total_students = len(df)

    avg_score = round(
        df["predicted_score"].mean(),
        2
    )

    pass_percent = round(

        (

            df["result"]
            .value_counts(normalize=True)
            .get("PASS", 0)

            * 100

        ),

        2

    )

    return {

        "total_students":
        total_students,

        "avg_score":
        avg_score,

        "pass_percent":
        pass_percent

    }


# ============================================================
# 2️⃣ WEAK STUDENTS
# ============================================================

def get_weak_students(df, threshold=50):

    if df.empty:

        return pd.DataFrame()

    weak_df = df[

        df["predicted_score"] < threshold

    ]

    return weak_df.sort_values(
        "predicted_score"
    )


# ============================================================
# 3️⃣ ATTENDANCE VS SCORE
# ============================================================

def attendance_vs_score(df):

    if df.empty:

        return None

    if "Attendance" not in df.columns:

        return None

    correlation = df["Attendance"].corr(

        df["predicted_score"]

    )

    if correlation > 0.6:

        message = (
            "Strong positive relation "
            "between attendance and performance."
        )

    elif correlation > 0.3:

        message = (
            "Moderate relation "
            "between attendance and performance."
        )

    else:

        message = (
            "Low relation "
            "between attendance and performance."
        )

    return correlation, message


# ============================================================
# 4️⃣ TEACHER RECOMMENDATIONS
# ============================================================

def teacher_recommendations(df):

    advice = []

    if df.empty:

        return [

            "No student data available yet."

        ]

    avg_score = df["predicted_score"].mean()

    avg_attendance = (

        df["Attendance"].mean()

        if "Attendance" in df.columns

        else 0

    )

    weak_students = df[

        df["predicted_score"] < 50

    ]

    # Low class performance
    if avg_score < 60:

        advice.append(

            "📘 Conduct revision classes "
            "for weak topics."

        )

    # Low attendance
    if avg_attendance < 70:

        advice.append(

            "📢 Encourage students "
            "to improve attendance."

        )

    # Weak students
    if len(weak_students) > 0:

        advice.append(

            f"⚠️ {len(weak_students)} "
            "students require mentoring."

        )

    # Good performance
    if not advice:

        advice.append(

            "✅ Overall class performance is good."

        )

    return advice


# ============================================================
# 5️⃣ DIFFICULTY ANALYSIS
# ============================================================

def difficulty_analysis(df):

    if df.empty:

        return "No data available."

    factors = {}

    # ========================================================
    # CHECK NEW DATASET FEATURES
    # ========================================================

    if "Study_Hours" in df.columns:

        factors["Study_Hours"] = (
            df["Study_Hours"].mean()
        )

    if "Attendance" in df.columns:

        factors["Attendance"] = (
            df["Attendance"].mean()
        )

    if "Previous_Marks" in df.columns:

        factors["Previous_Marks"] = (
            df["Previous_Marks"].mean()
        )

    if "Sleep_Hours" in df.columns:

        factors["Sleep_Hours"] = (
            df["Sleep_Hours"].mean()
        )

    if "Sports_Activity" in df.columns:

        factors["Sports_Activity"] = (
            df["Sports_Activity"].mean()
        )

    if not factors:

        return (
            "Not enough data "
            "to analyze performance."
        )

    weakest = min(

        factors,

        key=factors.get

    )

    return (

        f"Students are weakest in: {weakest}"

    )


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("=== TEST TEACHER DASHBOARD ===")

    data = {

        "Study_Hours":
        [10, 25, 18],

        "Attendance":
        [55, 80, 72],

        "Previous_Marks":
        [45, 75, 60],

        "Sleep_Hours":
        [5, 7, 6],

        "Sports_Activity":
        [1, 3, 2],

        "predicted_score":
        [48, 78, 65],

        "result":
        ["FAIL", "PASS", "PASS"],

        "grade":
        ["F", "A", "C"]

    }

    df = pd.DataFrame(data)

    print(

        "Class Summary:",
        class_summary(df)

    )

    print(

        "\nWeak Students:\n",
        get_weak_students(df)

    )

    print(

        "\nAttendance Impact:",
        attendance_vs_score(df)

    )

    print(

        "\nTeacher Advice:",
        teacher_recommendations(df)

    )

    print(

        "\nDifficulty:",
        difficulty_analysis(df)

    )