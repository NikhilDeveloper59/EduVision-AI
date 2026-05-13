"""
recommendation.py
------------------------------------
AI Recommendation Engine
Updated for New Student Dataset
"""

# ============================================================
# 1️⃣ RISK LEVEL CALCULATOR
# ============================================================

def calculate_risk(
    study_hours,
    attendance,
    previous_marks,
    sleep_hours,
    sports_activity,
    predicted_score
):

    risk_score = 0

    # Low study hours
    if study_hours < 20:
        risk_score += 2

    # Poor attendance
    if attendance < 60:
        risk_score += 2

    # Weak previous marks
    if previous_marks < 50:
        risk_score += 2

    # Poor sleep
    if sleep_hours < 5:
        risk_score += 1

    # Low physical activity
    if sports_activity < 2:
        risk_score += 1

    # Low predicted score
    if predicted_score < 50:
        risk_score += 2

    # Final Risk
    if risk_score >= 6:
        return "HIGH"

    elif risk_score >= 3:
        return "MEDIUM"

    else:
        return "LOW"


# ============================================================
# 2️⃣ STUDENT RECOMMENDATIONS
# ============================================================

def student_recommendations(
    study_hours,
    attendance,
    previous_marks,
    sleep_hours,
    sports_activity,
    predicted_score
):

    advice = []

    # Study hours
    if study_hours < 20:
        advice.append(
            "📘 Increase study hours regularly."
        )

    # Attendance
    if attendance < 75:
        advice.append(
            "🏫 Improve attendance percentage."
        )

    # Previous marks
    if previous_marks < 60:
        advice.append(
            "📝 Focus more on weak subjects."
        )

    # Sleep
    if sleep_hours < 6:
        advice.append(
            "😴 Take proper sleep daily."
        )

    # Sports activity
    if sports_activity < 2:
        advice.append(
            "⚽ Participate in sports or physical activity."
        )

    # Predicted performance
    if predicted_score < 50:
        advice.append(
            "👨‍🏫 Meet teachers for additional guidance."
        )

    # Excellent performance
    if predicted_score >= 75:
        advice.append(
            "✅ Excellent performance. Keep it up!"
        )

    # Default message
    if not advice:
        advice.append(
            "👍 Maintain your current performance."
        )

    return advice


# ============================================================
# 3️⃣ WEEKLY STUDY PLAN
# ============================================================

def generate_study_plan():

    return {

        "Monday":
        "Programming + Coding Practice",

        "Tuesday":
        "Database Management Revision",

        "Wednesday":
        "Lab Practice + Assignments",

        "Thursday":
        "Mock Test + MCQs",

        "Friday":
        "Weak Subject Revision",

        "Saturday":
        "Project Practice + Notes",

        "Sunday":
        "Revision + Rest"
    }


# ============================================================
# 4️⃣ EARLY WARNING MESSAGE
# ============================================================

def early_warning_message(risk_level):

    if risk_level == "HIGH":

        return (
            "🚨 HIGH RISK: "
            "Immediate academic improvement required."
        )

    elif risk_level == "MEDIUM":

        return (
            "⚠️ MEDIUM RISK: "
            "Improve study habits and attendance."
        )

    else:

        return (
            "✅ LOW RISK: "
            "You are performing well."
        )


# ============================================================
# 5️⃣ TESTING
# ============================================================

if __name__ == "__main__":

    print("=== TESTING RECOMMENDATION ENGINE ===")

    risk = calculate_risk(

        study_hours=15,
        attendance=55,
        previous_marks=45,
        sleep_hours=5,
        sports_activity=1,
        predicted_score=48

    )

    print("Risk Level:", risk)

    print("\nSuggestions:")

    tips = student_recommendations(

        15,
        55,
        45,
        5,
        1,
        48

    )

    for t in tips:

        print("-", t)

    print("\nStudy Plan:")

    print(generate_study_plan())