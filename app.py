import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Streamlit page config
st.set_page_config(page_title="Student Score Predictor", layout="centered")

# Title
st.title("Student Exam Score Prediction App")

st.markdown("""
This app predicts the **exam scores** based on input features like Gender, Ethnicity, Parental Education, Lunch, and Test Preparation Course.
""")

# Input form
with st.form("prediction_form"):
    gender = st.selectbox("Gender", ["male", "female"])
    race_ethnicity = st.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
    parental_level_of_education = st.selectbox("Parental Level of Education", 
                                              ["some high school", "high school", "some college", 
                                               "associate's degree", "bachelor's degree", "master's degree"])
    lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
    test_preparation_course = st.selectbox("Test Preparation Course", ["none", "completed"])
    reading_score = st.number_input("Reading Score", min_value=0.0, max_value=100.0, value=50.0)
    writing_score = st.number_input("Writing Score", min_value=0.0, max_value=100.0, value=50.0)

    submit_button = st.form_submit_button(label="Predict")

if submit_button:
    # Create data instance
    data = CustomData(
        gender=gender,
        race_ethnicity=race_ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=reading_score,
        writing_score=writing_score
    )

    pred_df = data.get_data_as_data_frame()
    st.write("### Input DataFrame:")
    st.dataframe(pred_df)

    # Predict
    predict_pipeline = PredictPipeline()
    try:
        results = predict_pipeline.predict(pred_df)
        st.success(f"Predicted Exam Score: **{results[0]:.2f}**")
    except Exception as e:
        st.error(f"Error in prediction: {e}")
