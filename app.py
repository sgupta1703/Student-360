import streamlit as st
from model import load_model, predict_gpa  
from datapreprocessing import preprocess_data, generate_visualizations
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

model = load_model('student_gpa_predictor.pkl')

def predict_page():
    st.subheader('Student Lifestyle GPA Predictor')
    data = preprocess_data()

    study_hours = st.slider('Study Hours Per Day', min_value=0, max_value=12, value=4)
    stress_level = st.selectbox('Stress Level', ['Low', 'Moderate', 'High'])
    sleep_hours = st.slider('Sleep Hours Per Night', min_value=0, max_value=12, value=6)
    screen_time = st.slider('Screen Time (Hours/Day)', min_value=0, max_value=10, value=3)
    exercise_freq = st.selectbox('Exercise Frequency', ['Daily', 'Weekly', 'Rarely'])
    
    stress_map = {'Low': 0, 'Moderate': 1, 'High': 2}
    stress_level = stress_map[stress_level]

    def provide_recommendations(study_hours, sleep_hours, stress_level, screen_time):
        if study_hours < 2:
            st.warning("Consider increasing study hours to improve your GPA.")
        if sleep_hours < 6:
            st.warning("Ensure you get at least 7-8 hours of sleep for better performance.")
        if stress_level == 2:
            st.info("Practice relaxation techniques like meditation or deep breathing.")
        if screen_time > 6:
            st.warning("Try reducing screen time to improve focus and productivity.")

    predicted_gpa = None
    if st.button('Predict GPA'):
        predicted_gpa = predict_gpa(model, study_hours, stress_level)
        st.write(f"Predicted GPA: {predicted_gpa:.2f}")
        provide_recommendations(study_hours, sleep_hours, stress_level, screen_time)
        try:
            data_limited = data[['GPA', 'Study_Hours_Per_Day']].iloc[:100]
        except KeyError:
            st.error("Column names mismatch! Ensure 'GPA' and 'Study_Hours_Per_Day' are present in the dataset.")
            st.stop()

        st.subheader("Real-time GPA Prediction Graph (Study Hours vs GPA)")
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        chart_placeholder = st.empty()
        chart_data = pd.DataFrame(columns=['Study_Hours_Per_Day', 'GPA'])

        for i in range(len(data_limited)):
            new_row = data_limited.iloc[i:i+1]
            chart_data = pd.concat([chart_data, new_row])
            status_text.text(f"{i+1}/{len(data_limited)} rows processed")
            chart_placeholder.line_chart(chart_data.set_index('Study_Hours_Per_Day'))
            progress_bar.progress((i + 1) / len(data_limited))
            time.sleep(0.02)

    def export_report():
        report_data = pd.DataFrame({
            'Study Hours': [study_hours],
            'Stress Level': [stress_level],
            'Sleep Hours': [sleep_hours],
            'Screen Time': [screen_time],
            'Exercise Frequency': [exercise_freq],
            'Predicted GPA': [predicted_gpa] if predicted_gpa is not None else ['Not Predicted']
        })
        report_data.to_csv('student_report.csv', index=False)
        with open('student_report.csv', 'rb') as file:
            st.download_button(
                label="Download Your Report",
                data=file,
                file_name='student_report.csv',
                mime='text/csv'
            )

    export_report()

def goals_page():
    st.subheader("Set Your Own Goals!")
    study_hours_goals = st.slider('I plan to study this many hours per day?', min_value=1, max_value=10, value=2)
    sleep_hours_goals = st.slider('I plan to sleep this many hours per day?', min_value=2, max_value=12, value=7)
    screen_time_goals = st.slider('I plan to watch this many hours of devices per day?', min_value=0, max_value=5, value=2)

    def export_goals_report():
        goals_data = pd.DataFrame({
            'Day Number': [0],
            'Study Hours Goal': [study_hours_goals],
            'Sleep Hours Goal': [sleep_hours_goals],
            'Screen Time Goal': [screen_time_goals],
        })
        goals_data.to_csv('my_goals_report.csv', index=False)
        with open('my_goals_report.csv', 'rb') as file:
            st.download_button(
                label="Download Your Goals Report",
                data=file,
                file_name='my_goals_report.csv',
                mime='text/csv'
            )

    export_goals_report()

def chatbot_page():
    st.subheader("Ask Our AI Chatbot")
    user_query = st.text_input("Ask me anything about GPA improvement, study habits, or app features:")
    if user_query:
        responses = {
            "study habits": "Consistent study schedules and short breaks improve productivity.",
            "GPA improvement": "Focus on time management, balanced sleep, and reducing stress levels.",
            "exercise": "Regular exercise boosts focus and memory retention.",
            "stress management": "Try mindfulness techniques like meditation and deep breathing exercises.",
            "app": "This app helps predict GPA based on lifestyle factors and provides recommendations.",
            "hello": "Hello! How can I assist you today?"
        }
        response = responses.get(user_query.lower(), "I'm here to help! Please ask specific questions about the app or study tips.")
        st.write(response)

def feedback_page():
    st.subheader("Feedback")
    feedback = st.text_area("We value your feedback! Please share your thoughts, suggestions, or issues you faced while using the app.")
    if st.button("Submit Feedback"):
        with open('feedback.txt', 'a') as f:
            f.write(feedback + '\n')
        st.success("Thank you for your feedback!")

st.markdown("<h1 style='text-align: center; font-family: Arial;'>Student 360</h1>", unsafe_allow_html=True)

page = st.sidebar.selectbox("Select a Page", ["GPA Predictor", "Set Goals", "AI Chatbot", "Feedback"])

if page == "GPA Predictor":
    predict_page()
elif page == "Set Goals":
    goals_page()
elif page == "AI Chatbot":
    chatbot_page()
elif page == "Feedback":
    feedback_page()
