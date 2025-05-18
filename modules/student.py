
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import random

# ------------------- Helper Function -------------------
def marks_to_grade(marks):
    if marks >= 90:
        return 'O'
    elif marks >= 80:
        return 'E'
    elif marks >= 70:
        return 'A'
    elif marks >= 60:
        return 'B'
    elif marks >= 50:
        return 'C'
    elif marks >= 40:
        return 'D'
    else:
        return 'F'

# ------------------- Login Page -------------------
def student_login(df):
    st.title("🎓 Student Grade & Performance System")
    st.subheader("🔐 Student Login")

    student_id = st.text_input("Student ID")
    password = st.text_input("Password", type="password")

    # Generate CAPTCHA
    if 'captcha_a' not in st.session_state:
        st.session_state.captcha_a = random.randint(1, 10)
        st.session_state.captcha_b = random.randint(1, 10)

    captcha_question = f"{st.session_state.captcha_a} + {st.session_state.captcha_b}"
    captcha_input = st.text_input(f" CAPTCHA: {captcha_question}")

    if st.button("Login"):
        try:
            captcha_answer = int(captcha_input)
        except ValueError:
            st.error("⚠️ Please enter a valid number for CAPTCHA.")
            st.stop()

        correct_answer = st.session_state.captcha_a + st.session_state.captcha_b

        if captcha_answer != correct_answer:
            st.error("❌ CAPTCHA failed. Try again.")
            st.session_state.captcha_a = random.randint(1, 10)
            st.session_state.captcha_b = random.randint(1, 10)
            st.stop()

        df["ID"] = df["ID"].astype(str)
        user_row = df[df["ID"] == student_id]

        if not user_row.empty and str(user_row.iloc[0]["Password"]) == password:
            st.session_state.logged_in = True
            st.session_state.student_data = user_row.iloc[0]
            st.success(f"✅ Welcome {user_row.iloc[0]['Name']}!")
            del st.session_state.captcha_a
            del st.session_state.captcha_b
            st.rerun()
        else:
            st.error("❌ Invalid ID or Password")

# ------------------- Dashboard -------------------

def student_dashboard(student_data, df):
    st.title("📊 Student Dashboard")
    st.markdown(f"### 👋 Welcome, **{student_data['Name']}**")

    tabs = st.tabs(["📋 Results", "📈 Comparison", "🔮 Prediction", "💡 Smart Recommendations"])

    # --- Tab 1: Results ---
    with tabs[0]:
        st.header("📘 Semester-wise Results")

        if 'sem_page' not in st.session_state:
            st.session_state.sem_page = 1

        sem = st.session_state.sem_page
        st.subheader(f"Semester {sem}")

        sem_cols = [f"Sem{sem}_Sub{i}" for i in range(1, 7)]
        cols = st.columns(3)

        max_marks = {col: df[col].max() if col in df.columns else 100 for col in sem_cols}

        subject_gpas = []
        for i, col in enumerate(sem_cols):
            with cols[i % 3]:
                if col in student_data:
                    mark = student_data[col]
                    grade = marks_to_grade(mark)
                    gpa = round((mark / max_marks[col]) * 10, 2) if max_marks[col] else 0
                    subject_gpas.append(gpa)
                    # st.metric(label=f"Subject {i+1}", value=f"{mark}", delta=f"Grade: {grade} | GPA: {gpa}")
                    # if mark >= 40:
                    #     color = 'green'
                    # else:
                    #     color = 'red'
                    # # Showing result without up arrow
                    # st.metric(label=f"Subject {i+1}", value=f"{mark}")
                    # st.markdown(f"<p style='color: {color}; '> Grade: {grade} | GPA: {gpa}</p>", unsafe_allow_html=True)
                    color = 'green' if mark >= 40 else 'red'

                    st.markdown(
                    f"""
                    <div style='margin-top: 20px; line-height:1.2; font-size: 30px;'>
                    <b>Subject {i+1}</b><br>
                    {mark}<br>
                    <span style='color: {color}; font-size: 18px;'>Grade: {grade} | GPA: {gpa}</span>
                    </div><br>
                    """,
                    unsafe_allow_html=True
                    )

                else:
                    st.info(f"Subject {i+1}: N/A")

        if subject_gpas:
            sgpa = round(sum(subject_gpas) / len(subject_gpas), 2)
            st.success(f"📘 **SGPA (Semester GPA)**: {sgpa}")
        else:
            sgpa = None

        all_sgpas = []
        for s in range(1, 7):
            temp_cols = [f"Sem{s}_Sub{i}" for i in range(1, 7)]
            temp_gpas = []
            for col in temp_cols:
                if col in student_data and col in df.columns:
                    mark = student_data[col]
                    max_mark = df[col].max()
                    gpa = round((mark / max_mark) * 10, 2) if max_mark else 0
                    temp_gpas.append(gpa)
            if temp_gpas:
                all_sgpas.append(sum(temp_gpas) / len(temp_gpas))

        if all_sgpas:
            cgpa = round(sum(all_sgpas) / len(all_sgpas), 2)
            st.info(f"🎓 **CGPA (Cumulative GPA)**: {cgpa}")

        nav_col1, nav_col2 = st.columns([1, 1])
        with nav_col1:
            if sem > 1 and st.button("⬅️ Previous"):
                st.session_state.sem_page -= 1
                st.rerun()
        with nav_col2:
            if f"Sem{sem+1}_Sub1" in student_data and st.button("Next ➡️"):
                st.session_state.sem_page += 1
                st.rerun()


    # --- Tab 2: Comparison ---
    with tabs[1]:
        st.header("📈 Semester-wise Performance Analysis")

        selected_sem = st.selectbox("Select Semester", [f"Semester {i}" for i in range(1, 7)])
        sem_number = selected_sem.split()[-1]

        subjects = [col for col in student_data.index if f"Sem{sem_number}_" in col and "Sub" in col]

        if not subjects:
            st.warning(f"No data available for {selected_sem}.")
        else:
            your_marks = [student_data[col] for col in subjects]
            class_avg = [df[col].mean() if col in df.columns else 0 for col in subjects]
            subject_labels = [col.replace("_", " ") for col in subjects]

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(subject_labels, your_marks, label="Your Marks", color="#4caf50", marker='o', linewidth=2)
            ax.plot(subject_labels, class_avg, label="Class Average", color="#f44336", linestyle='--', marker='x', linewidth=2)

            ax.set_title(f"Performance in {selected_sem}", fontsize=14)
            ax.set_xlabel("Subjects")
            ax.set_ylabel("Marks")
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.legend()

            plt.xticks(rotation=45)
            st.pyplot(fig)

    # --- Tab 3: Prediction ---
    with tabs[2]:
        st.header("🔮 Performance Prediction")

        # Reuse the same subjects from previous tab
        subjects = [col for col in student_data.index if f"Sem{st.session_state.sem_page}_" in col and "Sub" in col]
        your_marks = [student_data[col] for col in subjects if pd.notna(student_data[col])]

        X, y = [], []
        for _, row in df.iterrows():
            student_marks = [row[col] for col in subjects if pd.notna(row[col])]
            if len(student_marks) == len(subjects):
                X.append(student_marks)
                y.append(np.mean(student_marks))

        if X and y:
            if len(your_marks) == len(subjects):
                model = LinearRegression()
                model.fit(X, y)
                predicted_avg = model.predict([your_marks])[0]
                st.success(f"🎯 Predicted Next Semester Average: **{(predicted_avg)/10:.2f}** SGPA")
            else:
                st.warning("⚠️ Your data is incomplete for prediction.")
        else:
            st.warning("⚠️ Not enough data to generate prediction.")

        # --- Tab 4: Actionable Insights & Roadmap ---
    with tabs[3]:
        st.header("🎯 Actionable Insights & Roadmap")

        sem = st.session_state.sem_page
        subject_cols = [f"Sem{sem}_Sub{i}" for i in range(1, 7)]
        subject_names = [f"Subject {i}" for i in range(1, 7)]

        marks = [student_data[col] for col in subject_cols if col in student_data and pd.notna(student_data[col])]
        subjects = [subject_names[i] for i, col in enumerate(subject_cols) if col in student_data and pd.notna(student_data[col])]

        # --- 1. Highlights and Weaknesses ---
        st.subheader("📌 Strengths & Weak Areas")

        for i, mark in enumerate(marks):
            if mark >= 85:
                st.success(f"✅ {subjects[i]}: Excellent! Keep up the strong performance.")
            elif mark < 60:
                st.error(f"⚠️ {subjects[i]}: Needs Improvement. Focus more on this subject.")
            else:
                st.info(f"ℹ️ {subjects[i]}: Good effort. Try pushing for a higher grade.")


        # --- 2. Trend Chart 
        
       # --- Enhanced Trend Chart: Prefer Sem 5 & 6, else last two semesters ---
        sem_cols = [col for col in student_data.keys() if col.startswith("Sem") and "_Sub" in col]
        semester_numbers = sorted(set(int(col[3]) for col in sem_cols))

        sem_prev, sem_curr = None, None

# Prefer Sem 5 and 6 if both available
        if 5 in semester_numbers and 6 in semester_numbers:
         sem_prev, sem_curr = 5, 6
# Else pick the last two available semesters
        elif len(semester_numbers) >= 2:
         sem_prev, sem_curr = semester_numbers[-2], semester_numbers[-1]

        if sem_prev and sem_curr:
         prev_sem_cols = [f"Sem{sem_prev}_Sub{i}" for i in range(1, 7)]
         curr_sem_cols = [f"Sem{sem_curr}_Sub{i}" for i in range(1, 7)]

         prev_marks = [student_data.get(col) for col in prev_sem_cols if pd.notna(student_data.get(col))]
         curr_marks = [student_data.get(col) for col in curr_sem_cols if pd.notna(student_data.get(col))]

         valid_subjects = [f"Subject {i}" for i in range(1, len(prev_marks)+1)]

        if prev_marks and curr_marks:
         st.subheader(f"📈 Trend: Semester {sem_prev} vs Semester {sem_curr}")
         fig, ax = plt.subplots(figsize=(8, 4))
         ax.plot(valid_subjects, prev_marks[:len(valid_subjects)], marker='o', label=f"Semester {sem_prev}")
         ax.plot(valid_subjects, curr_marks[:len(valid_subjects)], marker='s', label=f"Semester {sem_curr}")
         ax.set_title("Subject-wise Performance Trend")
         ax.set_ylabel("Marks")
         ax.set_ylim(0, 100)
         ax.legend()
         ax.grid(True, linestyle="--", alpha=0.5)
         st.pyplot(fig)

    
        
        # --- 3. Personalized Roadmap ---
        st.subheader("🛠 Recommended Roadmap")

        if marks:
            low_subjects = [subjects[i] for i, m in enumerate(marks) if m < 60]
            high_subjects = [subjects[i] for i, m in enumerate(marks) if m >= 85]

            roadmap = []
            if low_subjects:
                roadmap.append(f"📚 Focus on improving: {', '.join(low_subjects)}")
            if high_subjects:
                roadmap.append(f"🌟 Maintain excellence in: {', '.join(high_subjects)}")
            roadmap.append("📆 Allocate weekly study time per subject.")
            roadmap.append("💡 Use college/external resources (YouTube, Coursera, etc).")

            for point in roadmap:
                st.write(f"- {point}")
        else:
            st.info("No subject data available to generate roadmap.")

        # --- 4. Achievement Badge (optional) ---
        if sgpa and sgpa >= 8.5:
            st.balloons()
            st.markdown("🏅 **Achievement Unlocked: High Performer!** You’ve maintained an SGPA above 8.5. Well done!")


    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.student_data = None
        st.rerun()

# ------------------- Main -------------------
def main():
    st.set_page_config(page_title="Student Performance System", layout="wide")

    # Sample data
    data = {
        'ID': ['1001', '1002'],
        'Password': ['pass123', 'secret'],
        'Name': ['Alice', 'Bob'],
        'Sem1_Sub1': [85, 78],
        'Sem1_Sub2': [78, 66],
        'Sem1_Sub3': [92, 70],
        'Sem1_Sub4': [88, 75],
        'Sem1_Sub5': [91, 80],
        'Sem1_Sub6': [84, 68],
        'Sem2_Sub1': [79, 72],
        'Sem2_Sub2': [80, 76],
        'Sem2_Sub3': [85, 70],
        'Sem2_Sub4': [88, 77],
        'Sem2_Sub5': [86, 71],
        'Sem2_Sub6': [90, 69]
    }

    df = pd.DataFrame(data)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.student_data = None

    if st.session_state.logged_in:
        student_dashboard(st.session_state.student_data, df)
    else:
        student_login(df)

if __name__ == "__main__":
    main()
