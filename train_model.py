# ============================================================
# FINAL TRAIN MODEL - AI Academic Support System
# FULLY UPDATED REAL METRICS VERSION
# ============================================================

import joblib
import pandas as pd
import json
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.metrics import (

    r2_score,
    accuracy_score,
    classification_report,

    mean_absolute_error,
    mean_squared_error,

    precision_score,
    recall_score,
    f1_score,

    confusion_matrix

)

from sklearn.linear_model import (

    LogisticRegression

)

from sklearn.ensemble import (

    GradientBoostingClassifier,
    RandomForestRegressor

)


# LOAD DATASET
df = pd.read_csv(
    "student_dataset.csv"
)

df.columns = df.columns.str.strip()

print(
    "✅ Dataset Loaded:",
    df.shape
)

# ============================================================
# DATA PREVIEW
# ============================================================

print("\nDataset Preview")

print(df.head())

# ============================================================
# REALISTIC PERFORMANCE SCORE GENERATION
# ============================================================

def generate_realistic_score(row):

    performance = str(
        row["Performance"]
    ).strip()

    study_hours = row["Study_Hours"]

    attendance = row["Attendance"]

    previous_marks = row["Previous_Marks"]

    sleep_hours = row["Sleep_Hours"]

    score = 0

    # ====================================================
    # BASE SCORE
    # ====================================================

    score += study_hours * 1.2

    score += attendance * 0.35

    score += previous_marks * 0.30

    score += sleep_hours * 1.5

    # ====================================================
    # RANDOM STUDENT BONUS
    # ====================================================

    score += np.random.randint(
        -5,
        12
    )

    # ====================================================
    # PERFORMANCE CATEGORY EFFECT
    # ====================================================

    if performance == "Poor":

        score -= np.random.randint(20, 35)

    elif performance == "Average":

        score += np.random.randint(-5, 8)

    elif performance == "Good":

        score += np.random.randint(8, 15)

    elif performance == "Excellent":

        score += np.random.randint(15, 22)

    # ====================================================
    # RANDOM NOISE
    # ====================================================

    score += np.random.normal(
        0,
        5
    )

    # ====================================================
    # FINAL LIMIT
    # ====================================================

    score = max(
        5,
        min(98, score)
    )

    return round(score)

df["Performance_Score"] = df.apply(

    generate_realistic_score,

    axis=1

)
# ============================================================
# REMOVE NULL DATA
# ============================================================

df = df.dropna()

print(
    "\n✅ Clean Dataset:",
    df.shape
)

# ============================================================
# PASS / FAIL
# ============================================================

df["result"] = df[
    "Performance_Score"
].apply(

    lambda x:1 if x >= 50 else 0

)

print("\nPass/Fail Distribution")

print(
    df["result"].value_counts()
)

# ============================================================
# GRADE SYSTEM
# ============================================================

def get_grade(score):

    if score >= 90:
        return "A+"

    elif score >= 78:
        return "A"

    elif score >= 60:
        return "B"

    elif score >= 40:
        return "C"
    else:
        return "F"

df["grade"] = df[
    "Performance_Score"
].apply(get_grade)

print("\nGrade Distribution")

print(
    df["grade"].value_counts()
)

# ============================================================
# FEATURE ENGINEERING
# ============================================================

df["study_efficiency"] = (

    df["Study_Hours"] *

    df["Attendance"]

)

df["health_factor"] = (

    df["Sleep_Hours"] *

    df["Sports_Activity"]

)

# ============================================================
# SAFE QUALITY MAP
# ============================================================

quality_map = {

    "Poor":1,
    "Average":2,
    "Good":3,
    "Excellent":4,

    "Low":1,
    "Medium":2,
    "High":3

}

# ============================================================
# TEACHER SUPPORT SCORE
# ============================================================

df["teacher_support_score"] = (

    df["Explanation_Quality"]
    .astype(str)
    .map(quality_map)
    .fillna(1)

    *

    df["Student_Interaction"]
    .astype(str)
    .map(quality_map)
    .fillna(1)

)

# ============================================================
# LAB USAGE
# ============================================================

df["lab_usage"] = (

    df["Lab_Facility"] *

    df["Lab_Timing"]

)

# FILL REMAINING NaN
df = df.fillna(0)

# LABEL ENCODING
encoders = {}

categorical_cols = df.select_dtypes(

    include=["object", "string"]

).columns

for col in categorical_cols:

    if col in [

        "Performance",
        "grade"

    ]:
        continue

    le = LabelEncoder()

    df[col] = le.fit_transform(

        df[col].astype(str)

    )

    encoders[col] = le

joblib.dump(

    encoders,
    "label_encoders.pkl"

)

print(
    "✅ Encoders Saved"
)


# FEATURES

all_features = df.drop(columns=[

    "Performance",
    "Performance_Score",
    "result",
    "grade"

]).columns.tolist()

important_features = all_features.copy()

X = df[all_features]


# TARGETS
y_reg = df["Performance_Score"]

y_pf = df["result"]

y_grade = df["grade"]

# ============================================================
# SAVE FEATURES
# ============================================================

joblib.dump(

    all_features,
    "all_features.pkl"

)

joblib.dump(

    important_features,
    "feature_columns.pkl"

)

# DEFAULT VALUES
default_values = {}

for col in all_features:

    default_values[col] = float(

        df[col].median()

    )

with open(

    "default_feature_values.json",
    "w"

) as f:

    json.dump(
        default_values,
        f
    )

print(
    "✅ Feature Files Saved"
)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y_reg,

    test_size=0.2,

    random_state=42

)

# REGRESSION MODEL
reg_model = RandomForestRegressor(

    n_estimators=300,

    random_state=42

)

reg_model.fit(

    X_train,
    y_train

)

pred_reg = reg_model.predict(
    X_test
)

# REGRESSION METRICS

reg_r2 = r2_score(

    y_test,
    pred_reg

)

mae = mean_absolute_error(

    y_test,
    pred_reg

)

mse = mean_squared_error(

    y_test,
    pred_reg

)

rmse = np.sqrt(mse)

print(

    "\n✅ Regression R²:",
    round(reg_r2, 3)

)

print(
    "✅ MAE:",
    round(mae, 3)
)

print(
    "✅ MSE:",
    round(mse, 3)
)

print(
    "✅ RMSE:",
    round(rmse, 3)
)

joblib.dump(

    reg_model,
    "regression_model.pkl"

)

# ============================================================
# PASS FAIL MODEL
# ============================================================

X_train_pf, X_test_pf, y_train_pf, y_test_pf = train_test_split(

    X,
    y_pf,

    test_size=0.2,

    stratify=y_pf,

    random_state=42

)

pf_model = Pipeline([

    (

        "scaler",

        StandardScaler()

    ),

    (

        "clf",

        LogisticRegression(
            max_iter=1000
        )

    )

])

pf_model.fit(

    X_train_pf,
    y_train_pf

)

pred_pf = pf_model.predict(
    X_test_pf
)

# ============================================================
# PASS FAIL METRICS
# ============================================================

pf_acc = accuracy_score(

    y_test_pf,
    pred_pf

)

pf_precision = precision_score(

    y_test_pf,
    pred_pf

)

pf_recall = recall_score(

    y_test_pf,
    pred_pf

)

pf_f1 = f1_score(

    y_test_pf,
    pred_pf

)

pf_cm = confusion_matrix(

    y_test_pf,
    pred_pf

).tolist()

print(

    "\n✅ Pass/Fail Accuracy:",
    round(pf_acc, 3)

)

print(

    classification_report(

        y_test_pf,
        pred_pf

    )

)

joblib.dump(

    pf_model,
    "pass_fail_model.pkl"

)

# ============================================================
# GRADE MODEL
# ============================================================

X_train_gr, X_test_gr, y_train_gr, y_test_gr = train_test_split(

    X,
    y_grade,

    test_size=0.2,

    stratify=y_grade,

    random_state=42

)

grade_model = GradientBoostingClassifier(

    n_estimators=300,

    learning_rate=0.05,

    max_depth=4,

    random_state=42

)

grade_model.fit(

    X_train_gr,
    y_train_gr

)

pred_grade = grade_model.predict(
    X_test_gr
)

# ============================================================
# GRADE METRICS
# ============================================================

grade_acc = accuracy_score(

    y_test_gr,
    pred_grade

)

grade_precision = precision_score(

    y_test_gr,
    pred_grade,

    average="weighted"

)

grade_recall = recall_score(

    y_test_gr,
    pred_grade,

    average="weighted"

)

grade_f1 = f1_score(

    y_test_gr,
    pred_grade,

    average="weighted"

)

print(

    "\n✅ Grade Accuracy:",
    round(grade_acc, 3)

)

print(

    classification_report(

        y_test_gr,
        pred_grade

    )

)

joblib.dump(

    grade_model,
    "grade_model.pkl"

)

# ============================================================
# SAVE MODEL METRICS
# ============================================================
results = {

    # ========================================================
    # REGRESSION
    # ========================================================

    "Regression_R2":
    float(reg_r2),

    "MAE":
    float(mae),

    "MSE":
    float(mse),

    "RMSE":
    float(rmse),

    # ========================================================
    # PASS FAIL
    # ========================================================

    "PassFail_Accuracy":
    float(pf_acc),

    "PassFail_Precision":
    float(pf_precision),

    "PassFail_Recall":
    float(pf_recall),

    "PassFail_F1":
    float(pf_f1),

    "PassFail_CM":
    pf_cm,

    # ========================================================
    # GRADE
    # ========================================================

    "Grade_Accuracy":
    float(grade_acc),

    "Grade_Precision":
    float(grade_precision),

    "Grade_Recall":
    float(grade_recall),

    "Grade_F1":
    float(grade_f1),

    # ========================================================
    # GRADE DISTRIBUTION
    # ========================================================

    "Grade_Distribution":

        df["grade"]
        .value_counts()
        .sort_index()
        .to_dict()

}

with open(

    "model_metrics.json",
    "w"

) as f:

    json.dump(

        results,
        f,

        indent=4

    )

print(
    "\n✅ Model Metrics Saved"
)

# ============================================================
# FEATURE IMPORTANCE
# ============================================================

importance_df = pd.DataFrame({

    "Feature":
    all_features,

    "Importance":
    grade_model.feature_importances_

})

importance_df = importance_df.sort_values(

    "Importance",

    ascending=False

)

importance_df.to_csv(

    "feature_importance.csv",

    index=False

)

print(
    "\n✅ Feature Importance Saved"
)

# ============================================================
# FINAL SUMMARY
# ============================================================

print(

    "\nMinimum Score:",

    df["Performance_Score"].min()

)

print(

    "Maximum Score:",

    df["Performance_Score"].max()

)

print(
    "\n✅ MODEL TRAINING COMPLETE"
)