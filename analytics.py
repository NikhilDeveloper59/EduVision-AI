import sqlite3
import pandas as pd

# ============================================================
# DATABASE
# ============================================================

DB = "students.db"


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    try:

        conn = sqlite3.connect(DB)

        df = pd.read_sql(
            "SELECT * FROM records",
            conn
        )

        conn.close()

        return df

    except Exception as e:

        print("Analytics Error:", e)

        return pd.DataFrame()


# ============================================================
# GRADE SUMMARY
# ============================================================

def grade_summary(df):

    if df.empty:

        return pd.Series()

    # Updated grades
    grades = [

        "A+",
        "A",
        "B",
        "C",
        "D",
        "F"

    ]

    count = (

        df["grade"]

        .value_counts()

        .reindex(
            grades,
            fill_value=0
        )

    )

    return count


# ============================================================
# PASS FAIL SUMMARY
# ============================================================

def pass_fail_summary(df):

    if df.empty:

        return 0, 0, 0

    total = len(df)

    pass_count = len(

        df[
            df["result"] == "PASS"
        ]

    )

    fail_count = len(

        df[
            df["result"] == "FAIL"
        ]

    )

    return (

        pass_count,
        fail_count,
        total

    )


# ============================================================
# AVERAGE PERFORMANCE
# ============================================================

def average_score(df):

    if df.empty:

        return 0

    return round(

        df["predicted_score"].mean(),

        2

    )


# ============================================================
# TOP STUDENTS
# ============================================================

def top_students(df, top_n=5):

    if df.empty:

        return pd.DataFrame()

    return df.sort_values(

        "predicted_score",
        ascending=False

    ).head(top_n)


# ============================================================
# WEAK STUDENTS
# ============================================================

def weak_students(df, threshold=50):

    if df.empty:

        return pd.DataFrame()

    return df[

        df["predicted_score"] < threshold

    ].sort_values(

        "predicted_score"

    )


# ============================================================
# ATTENDANCE ANALYSIS
# ============================================================

def attendance_analysis(df):

    if df.empty:

        return 0

    if "Attendance" not in df.columns:

        return 0

    return round(

        df["Attendance"].mean(),

        2

    )


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    data = load_data()

    print("\n=== ANALYTICS TEST ===")

    print(

        "\nGrade Summary:\n",

        grade_summary(data)

    )

    print(

        "\nPass/Fail Summary:\n",

        pass_fail_summary(data)

    )

    print(

        "\nAverage Score:\n",

        average_score(data)

    )

    print(

        "\nTop Students:\n",

        top_students(data)

    )

    print(

        "\nWeak Students:\n",

        weak_students(data)

    )

    print(

        "\nAverage Attendance:\n",

        attendance_analysis(data)

    )