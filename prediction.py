import pandas as pd
import joblib
import json

# ============================================================
# LOAD MODELS
# ============================================================

reg_model = joblib.load(
    "regression_model.pkl"
)

pass_model = joblib.load(
    "pass_fail_model.pkl"
)

grade_model = joblib.load(
    "grade_model.pkl"
)

all_features = joblib.load(
    "all_features.pkl"
)


# DEFAULT VALUES
with open("default_feature_values.json") as f:

    default_values = json.load(f)

# ============================================================
# MAIN FUNCTION
# ============================================================

def predict_student(form_data):

    user_data = default_values.copy()

    # ============================================================
    # TEACHER PANEL DEFAULT VALUES
    # ============================================================

    study_hours = float(
        form_data.get("study_hours", 6)
    )

    sleep_hours = float(
        form_data.get("sleep_hours", 7)
    )

    sports_activity = float(
        form_data.get("sports_activity", 3)
    )

    explanation_quality = float(
        form_data.get("explanation_quality", 3)
    )

    student_interaction = float(
        form_data.get("student_interaction", 2)
    )

    lab_facility = float(
        form_data.get("lab_facility", 3)
    )

    teacher_support = float(
        form_data.get("teacher_support", 3)
    )

    library_usage = float(
        form_data.get("library_usage", 3)
    )

    exam_preparation = float(
        form_data.get("exam_preparation", 5)
    )

    learning_hours = float(
        form_data.get("learning_hours", 5)
    )

    project_submission = float(
        form_data.get("project_submission", 8)
    )

    internet_access = float(
        form_data.get("internet_access", 1)
    )

    # ALL FEATURES FROM WEBPAGE
    user_data["Study_Hours"] = study_hours

    user_data["Attendance"] = float(
        form_data.get("attendance", 0)
    )

    user_data["Previous_Marks"] = float(
        form_data.get("previous_marks", 0)
    )

    user_data["Sleep_Hours"] = sleep_hours

    user_data["Sports_Activity"] = sports_activity

    user_data["Explanation_Quality"] = explanation_quality

    user_data["Student_Interaction"] = student_interaction

    user_data["Lab_Facility"] = lab_facility

    user_data["Lab_Timing"] = float(
        form_data.get("lab_timing", 0)
    )

    # ========================================================
    # EXTRA FEATURES
    # ADD YOUR REMAINING FEATURES HERE
    # ========================================================

    user_data["Assignment_Completion"] = float(
        form_data.get("assignment_completion", 0)
    )

    user_data["Teacher_Support"] = teacher_support

    user_data["Internet_Access"] = internet_access

    user_data["Library_Usage"] = library_usage

    user_data["Class_Participation"] = float(
        form_data.get("class_participation", 0)
    )

    user_data["Exam_Preparation"] = exam_preparation

    user_data["Learning_Hours"] = learning_hours

    user_data["Project_Submission"] = project_submission

    # ========================================================
    # FEATURE ENGINEERING
    # ========================================================

    user_data["study_efficiency"] = (

        user_data["Study_Hours"]

        *

        user_data["Attendance"]

    )

    user_data["health_factor"] = (

        user_data["Sleep_Hours"]

        *

        user_data["Sports_Activity"]

    )

    user_data["teacher_support"] = (

        user_data["Explanation_Quality"]

        *

        user_data["Student_Interaction"]

    )

    user_data["lab_usage"] = (

        user_data["Lab_Facility"]

        *

        user_data["Lab_Timing"]

    )

    # ========================================================
    # DATAFRAME
    # ========================================================

    new_data = pd.DataFrame([user_data])

    new_data = new_data.reindex(
        columns=all_features,
        fill_value=0
    )


    # ========================================================
    # PREDICTION
    # ========================================================

    predicted_score = round(

        float(

            reg_model.predict(
                new_data
            )[0]

        ),

        2

    )
    grade = grade_model.predict(
        new_data
    )[0]

#   Assigning Grades
    if predicted_score >= 90:
        grade = "A+"

    elif predicted_score >= 80:
        grade = "A"

    elif predicted_score >= 70:
        grade = "B"

    elif predicted_score >= 60:
        grade = "C"

    elif predicted_score >= 40:
        grade = "D"

    else:
        grade = "F"

    if predicted_score >= 40:
        result = "PASS"
    else:
        result = "FAIL"
    

    # ========================================================
    # RISK LEVEL
    # ========================================================

    if predicted_score >= 75:

        risk = "LOW"

    elif predicted_score >= 55:

        risk = "MEDIUM"

    else:

        risk = "HIGH"

    # ========================================================
    # SUGGESTIONS
    # ========================================================

    suggestions = []

    if user_data["Attendance"] < 60:

        suggestions.append(
            "Improve attendance."
        )

    if user_data["Study_Hours"] < 20:

        suggestions.append(
            "Increase study hours."
        )

    if user_data["Sleep_Hours"] < 5:

        suggestions.append(
            "Sleep properly."
        )

    if predicted_score < 50:

        suggestions.append(
            "Need serious improvement."
        )

    if predicted_score >= 75:

        suggestions.append(
            "Excellent performance."
        )

    # ========================================================
    # WEEKLY PLAN
    # ========================================================

    weekly_plan = {

        "Monday":
        "Programming Practice",

        "Tuesday":
        "Database Revision",

        "Wednesday":
        "Lab Practice",

        "Thursday":
        "Mock Test",

        "Friday":
        "Assignments",

        "Saturday":
        "Weak Subject Revision",

        "Sunday":
        "Rest + Revision"

    }

    # ========================================================
    # FINAL RETURN
    # ========================================================

    return {

        "predicted_score":
        predicted_score,

        "result":
        result,

        "grade":
        grade,

        "risk":
        risk,

        "attendance":
        user_data["Attendance"],

        "previous_score":
        user_data["Previous_Marks"],

        "suggestions":
        suggestions,

        "weekly_plan":
        weekly_plan

    }

