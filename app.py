import streamlit as st
import numpy as np
import joblib
import warnings

warnings.filterwarnings("ignore")

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Student Exam Score Predictor",
    page_icon="🎓",
    layout="centered"
)

# -------------------------------
# LOAD MODEL
# -------------------------------
model = joblib.load("best_model.pkl")

# -------------------------------
# CUSTOM STYLING
# -------------------------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.big-card {
    background: linear-gradient(135deg,#4CAF50,#2196F3);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
}

.small-card {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.tip-box {
    border-left: 5px solid #4CAF50;
    padding: 10px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<h1 style='text-align:center;'>
🎓 Student Exam Score Predictor
</h1>

<p style='text-align:center;font-size:18px;color:gray;'>
Discover how study habits, attendance, sleep, and well-being
can influence academic performance.
</p>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------
# USER INPUTS
# -------------------------------
st.subheader("📋 Student Information")

study_hours = st.slider(
    "📚 Study Hours Per Day",
    0.0, 12.0, 4.0
)

attendance = st.slider(
    "🏫 Attendance Percentage",
    0.0, 100.0, 80.0
)

mental_health = st.slider(
    "🧠 Mental Health Rating",
    1, 10, 7
)

sleep_hours = st.slider(
    "😴 Sleep Hours Per Night",
    0.0, 12.0, 7.0
)

part_time_job = st.selectbox(
    "💼 Part-Time Job",
    ["No", "Yes"]
)

st.divider()

# -------------------------------
# QUICK SUMMARY
# -------------------------------
st.subheader("📊 Current Profile")

col1, col2 = st.columns(2)

with col1:
    st.metric("Study Hours", f"{study_hours:.1f}")
    st.metric("Mental Health", mental_health)

with col2:
    st.metric("Attendance", f"{attendance:.1f}%")
    st.metric("Sleep", f"{sleep_hours:.1f} hrs")

st.divider()

# -------------------------------
# PREDICTION
# -------------------------------
if st.button("🚀 Predict Exam Score", use_container_width=True):

    # Model trained on 4 features
    input_data = np.array([[
        study_hours,
        attendance,
        mental_health,
        sleep_hours
    ]])

    prediction = model.predict(input_data)[0]

    prediction = max(0, min(100, prediction))

    # Score Card
    st.markdown(
        f"""
        <div class="big-card">
        🎯 Predicted Score: {prediction:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Progress Bar
    st.progress(int(prediction))

    # Grade
    if prediction >= 90:
        grade = "A+"
        st.success("🌟 Outstanding Performance Expected!")
    elif prediction >= 80:
        grade = "A"
        st.success("🏆 Excellent Performance Expected!")
    elif prediction >= 70:
        grade = "B"
        st.info("👍 Good Performance Expected!")
    elif prediction >= 60:
        grade = "C"
        st.warning("🙂 Average Performance Expected!")
    else:
        grade = "D"
        st.error("📚 More Preparation Recommended!")

    st.metric("Estimated Grade", grade)

    st.divider()

    # Personalized Insights
    st.subheader("💡 Personalized Insights")

    if study_hours < 3:
        st.warning(
            "📚 Your study time is relatively low. Increasing daily study hours could improve your score."
        )

    if attendance < 75:
        st.warning(
            "🏫 Attendance is below the recommended level. Regular attendance often improves understanding and performance."
        )

    if sleep_hours < 6:
        st.warning(
            "😴 Sleep is important for memory and concentration. Consider getting more rest."
        )

    if mental_health < 5:
        st.warning(
            "🧠 Mental well-being can significantly impact academic performance. Take time to manage stress and maintain balance."
        )

    if (
        study_hours >= 6
        and attendance >= 80
        and sleep_hours >= 7
        and mental_health >= 7
    ):
        st.success(
            "🚀 Excellent balance of study habits, attendance, sleep, and mental health!"
        )

    st.divider()

    # Fun Interpretation
    st.subheader("📝 Performance Interpretation")

    if prediction >= 90:
        st.write(
            "You are showing the characteristics of a highly prepared student. Keep maintaining consistency."
        )

    elif prediction >= 75:
        st.write(
            "You are on a strong track. A few small improvements could boost your performance even further."
        )

    elif prediction >= 60:
        st.write(
            "Your foundation is decent, but there are opportunities to improve your habits and maximize results."
        )

    else:
        st.write(
            "Your current profile suggests room for improvement. Focus on attendance, study time, and healthy routines."
        )

# -------------------------------
# FOOTER
# -------------------------------
st.divider()

st.caption(
    "Built with ❤️ using Python, Scikit-Learn, Streamlit, and Machine Learning"
)