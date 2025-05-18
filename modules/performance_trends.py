import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def department_analytics_dashboard(df):
    st.title("📊 Admin Analytics Dashboard")

    # --- Extract subject columns ---
    subject_columns = [col for col in df.columns if "Sub" in col and "Sem" in col]
    if not subject_columns:
        st.warning("No subject data found in the dataset.")
        return

    # GPA calculation
    gpa_df = df[["ID", "Name"]].copy()
    gpa_data = df[subject_columns].applymap(lambda x: round((x / 100) * 10, 2))
    gpa_df = pd.concat([gpa_df, gpa_data], axis=1)

    semester_sgpas = {}
    for sem in range(1, 7):  # Assuming 6 semesters
        sem_cols = [col for col in subject_columns if f"Sem{sem}_" in col]
        if sem_cols:
            semester_sgpas[f"SGPA_Sem{sem}"] = gpa_data[sem_cols].mean(axis=1)
    for k, v in semester_sgpas.items():
        gpa_df[k] = v
    sgpa_cols = [col for col in gpa_df.columns if "SGPA" in col]
    gpa_df["CGPA"] = gpa_df[sgpa_cols].mean(axis=1)

    # Failure and pass rate calculation
    failure_counts = (df[subject_columns] < 40).sum()
    failure_rates = (failure_counts / len(df)) * 100
    failure_df = pd.DataFrame({"Subject": failure_rates.index, "Failure Rate (%)": failure_rates.values}).sort_values(by="Failure Rate (%)", ascending=False).head(10)

    pass_counts = (df[subject_columns] >= 40).sum()
    pass_rates = (pass_counts / len(df)) * 100
    pass_df = pd.DataFrame({"Subject": pass_rates.index, "Pass Rate (%)": pass_rates.values}).sort_values(by="Pass Rate (%)", ascending=False).head(10)

    # Semester-wise failure and pass rates
    sem_fail_data, sem_pass_data = [], []
    for sem in range(1, 7):
        sem_cols = [col for col in subject_columns if f"Sem{sem}_" in col]
        if sem_cols:
            fail_rate = (df[sem_cols] < 40).sum(axis=1) / len(sem_cols) * 100
            pass_rate = (df[sem_cols] >= 40).sum(axis=1) / len(sem_cols) * 100
            sem_fail_data.append((f"Sem{sem}", fail_rate.mean()))
            sem_pass_data.append((f"Sem{sem}", pass_rate.mean()))
    sem_fail_df = pd.DataFrame(sem_fail_data, columns=["Semester", "Average Failure Rate (%)"])
    sem_pass_df = pd.DataFrame(sem_pass_data, columns=["Semester", "Average Pass Rate (%)"])

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Top 10 Performers", 
        "Subjects with Highest Failure Rates", 
        "Subjects with Highest Pass Rates", 
        "Semester-wise Failure Rates", 
        "Semester-wise Pass Rates"
    ])

    # --- Tab 1: Top 10 Performers ---
    with tab1:
        st.subheader("🏆 Top 10 Performers (Tabular)")
        top_10 = gpa_df.sort_values(by="CGPA", ascending=False).head(10)
        top_10_display = top_10[["ID", "Name", "CGPA"]].reset_index(drop=True)
        top_10_display.index += 1
        st.dataframe(top_10_display, use_container_width=True)

        st.subheader("📈 Top 10 CGPA Chart")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.bar(top_10["Name"], top_10["CGPA"], color='green')
        ax1.set_xlabel("Student Name")
        ax1.set_ylabel("CGPA")
        ax1.set_ylim(7.25, 7.75)
        ax1.set_xticklabels(top_10["Name"], rotation=45, ha="right")
        ax1.set_title("Top 10 Students by CGPA")
        st.pyplot(fig1)

    # --- Tab 2: Subjects with Highest Failure Rates ---
    with tab2:
        st.subheader("❌ Subjects with Highest Failure Rates (Tabular)")
        failure_df_display = failure_df.reset_index(drop=True)
        failure_df_display.index += 1
        st.dataframe(failure_df_display, use_container_width=True)

        st.subheader("📊 Top 10 Subjects by Failure Rate")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.bar(failure_df["Subject"], failure_df["Failure Rate (%)"], color='red')
        ax2.set_xlabel("Subject")
        ax2.set_ylabel("Failure Rate (%)")
        ax2.set_ylim(10, 20)
        ax2.set_xticklabels(failure_df["Subject"], rotation=45, ha="right")
        ax2.set_title("Subjects with Highest Failure Rates")
        st.pyplot(fig2)

    # --- Tab 3: Subjects with Highest Pass Rates ---
    with tab3:
        st.subheader("✅ Subjects with Highest Pass Rates (Tabular)")
        pass_df_display = pass_df.reset_index(drop=True)
        pass_df_display.index += 1
        st.dataframe(pass_df_display, use_container_width=True)

        st.subheader("📊 Top 10 Subjects by Pass Rate")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.bar(pass_df["Subject"], pass_df["Pass Rate (%)"], color='blue')
        ax3.set_xlabel("Subject")
        ax3.set_ylabel("Pass Rate (%)")
        ax3.set_ylim(80, 90)
        ax3.set_xticklabels(pass_df["Subject"], rotation=45, ha="right")
        ax3.set_title("Subjects with Highest Pass Rates")
        st.pyplot(fig3)

    # --- Tab 4: Semester-wise Failure Rates ---
    with tab4:
        st.subheader("📉 Semester-wise Average Failure Rates")
        st.dataframe(sem_fail_df, use_container_width=True)

        fig4, ax4 = plt.subplots(figsize=(8, 5))
        ax4.bar(sem_fail_df["Semester"], sem_fail_df["Average Failure Rate (%)"], color="orange")
        ax4.set_ylim(10, 20)
        ax4.set_xlabel("Semester")
        ax4.set_ylabel("Failure Rate (%)")
        ax4.set_title("Semester-wise Failure Rates")
        st.pyplot(fig4)

    # --- Tab 5: Semester-wise Pass Rates ---
    with tab5:
        st.subheader("📈 Semester-wise Average Pass Rates")
        st.dataframe(sem_pass_df, use_container_width=True)

        fig5, ax5 = plt.subplots(figsize=(8, 5))
        ax5.bar(sem_pass_df["Semester"], sem_pass_df["Average Pass Rate (%)"], color="teal")
        ax5.set_ylim(80, 90)
        ax5.set_xlabel("Semester")
        ax5.set_ylabel("Pass Rate (%)")
        ax5.set_title("Semester-wise Pass Rates")
        st.pyplot(fig5)
