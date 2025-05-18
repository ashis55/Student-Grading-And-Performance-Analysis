import streamlit as st
import pandas as pd
from datetime import datetime

admin_credentials = {
    "admin001": "admin@123",
    "admin002": "admin@456"
}

current_time = datetime.now()

def admin_dashboard():
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.title("🔐 Admin Login")

        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if user_id in admin_credentials and admin_credentials[user_id] == password:
                st.success("✅ Login successful!")
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid user ID or password.")
        return

    # === Admin Dashboard ===
    st.title("🛡️ Admin Dashboard")
    tab_titles = ["📢 Announcements", "📰 News & Events", "🎓 Student Management"]
    tabs = st.tabs(tab_titles)

    # --- Tab 1: Announcements ---
    with tabs[0]:
        st.subheader("📢 Manage Announcements")
        title = st.text_input("Announcement Title")
        date = st.date_input("Date", value=datetime.today())
        description = st.text_area("Description")

        if st.button("Add Announcement"):
            new_data = pd.DataFrame([[title, date, description, current_time]], 
                                    columns=["title", "date", "description", "uploaded_at"])
            try:
                old_data = pd.read_excel("data/notices.xlsx", engine="openpyxl")
                final_df = pd.concat([old_data, new_data], ignore_index=True)
            except:
                final_df = new_data
            final_df.to_excel("data/notices.xlsx", index=False)
            st.success("✅ Announcement added!")

        st.markdown("---")
        st.subheader("📢 All Announcements")
        try:
            notice_df = pd.read_excel("data/notices.xlsx", engine="openpyxl")
            for _, row in notice_df.iterrows():
                with st.expander(f"{row['title']}  |  Date: {row['date'].strftime('%d/%m/%Y')}"):
                    st.write(row["description"])
        except:
            st.info("No announcements yet.")

        st.markdown("---")
        if st.button("🔓 Logout", key="logout_1"):
            st.session_state.admin_logged_in = False
            st.rerun()

    # --- Tab 2: News & Events ---
    with tabs[1]:
        st.subheader("📰 Manage News & Events")
        news_title = st.text_input("News Title")
        news_date = st.date_input("News Date", key="news_date")
        news_description = st.text_area("News Description")

        if st.button("Add News"):
            new_data = pd.DataFrame([[news_title, news_date, news_description, current_time]], 
                                    columns=["title", "date", "description", "uploaded_at"])
            try:
                old_data = pd.read_excel("data/news_events.xlsx", engine="openpyxl")
                final_df = pd.concat([old_data, new_data], ignore_index=True)
            except:
                final_df = new_data
            final_df.to_excel("data/news_events.xlsx", index=False)
            st.success("✅ News item added!")

        st.markdown("---")
        st.subheader("📰 All News & Events")
        try:
            news_df = pd.read_excel("data/news_events.xlsx", engine="openpyxl")
            for _, row in news_df.iterrows():
                with st.expander(f"{row['title']}  |  Date: {row['date'].strftime('%d/%m/%Y')}"):
                    st.write(row["description"])
        except:
            st.info("No news items yet.")

        st.markdown("---")
        if st.button("🔓 Logout", key="logout_2"):
            st.session_state.admin_logged_in = False
            st.rerun()

    # --- Tab 3: Student Management ---
    with tabs[2]:
        st.subheader("🎓 Manage Student Records")
        file_path = "data/student_data.xlsx"
        try:
            df = pd.read_excel(file_path, engine="openpyxl")

            # --- Sub-tabs for student management ---
            student_tab_titles = ["👁️ View Students", "➕ Add New Student", "✏️ Edit Student"]
            student_tabs = st.tabs(student_tab_titles)

            # --- Sub-tab 1: View Students ---
            with student_tabs[0]:
                st.subheader("👁️ View All Students")
                # 🔍 Search
                search_query = st.text_input("🔍 Search by ID or Name")
                if search_query:
                    filtered_df = df[df["ID"].astype(str).str.contains(search_query, case=False) |
                                     df["Name"].str.contains(search_query, case=False)]
                else:
                    filtered_df = df

                st.write("### 📋 Student List")
                st.dataframe(filtered_df)

            # --- Sub-tab 2: Add New Student ---
            with student_tabs[1]:
                st.subheader("➕ Add New Student")

                # Input fields for student details
                new_id = st.text_input("Student ID")
                new_name = st.text_input("Student Name")
                new_password = st.text_input("Password", type="password", key="new_student_password")

                # Define semesters and input fields for marks
                semesters = [f"Sem{i}_Sub{j}" for i in range(1, 7) for j in range(1, 7)]
                new_marks = {}
                with st.expander("Enter Marks for All Semesters"):
                    for col in semesters:
                        new_marks[col] = st.number_input(f"{col}", min_value=0, max_value=100, value=0)

                # When "Add Student" button is pressed
                if st.button("📥 Add Student"):
                    if new_id in df["ID"].values:
                        st.warning("⚠️ Student ID already exists.")
                    else:
                        # Create new student data
                        new_student = {
                            "ID": new_id,
                            "Name": new_name,
                            "Password": new_password,  # Use the value entered in the password field
                            "Grade": "",
                            **new_marks
                        }
                        # Add the new student data to the DataFrame
                        df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
                        # Save the updated DataFrame to the Excel file
                        df.to_excel(file_path, index=False)

                        # Show success message after adding the student
                        st.success("✅ New student added successfully!")

                        # Clear the input fields (Reset them)
                        new_id = ''
                        new_name = ''
                        new_password = ''  # Reset password field
                        for col in semesters:
                            new_marks[col] = 0  # Reset marks fields
                        
                        # Refresh the UI after adding the student
                        st.rerun()

            # --- Sub-tab 3: Edit Student ---
            with student_tabs[2]:
                st.subheader("✏️ Edit Existing Student")

                student_ids = df["ID"].tolist()
                selected_id = st.selectbox("Select Student ID", student_ids)

                if selected_id:
                    student_row = df[df["ID"] == selected_id].iloc[0]

                    new_name = st.text_input("Name", value=student_row["Name"], key="edit_name")
                    new_password = st.text_input("Password", value=student_row["Password"], key="edit_pass")

                    sem = st.selectbox("Semester", [f"Sem{i}" for i in range(1, 7)], key="edit_sem")
                    subject_marks = {}
                    st.write(f"📘 Edit marks for {sem}")
                    for i in range(1, 7):
                        col_name = f"{sem}_Sub{i}"
                        subject_marks[col_name] = st.number_input(
                            f"{col_name}", value=int(student_row[col_name]), min_value=0, max_value=100, key=col_name
                        )

                    if st.button("✅ Update Student Record"):
                        idx = df[df["ID"] == selected_id].index[0]
                        df.at[idx, "Name"] = new_name
                        df.at[idx, "Password"] = new_password
                        for col, val in subject_marks.items():
                            df.at[idx, col] = val
                        df.to_excel(file_path, index=False)
                        st.success("Student record updated successfully!")
                        st.rerun()

        except FileNotFoundError:
            st.warning("Student data file not found.")
        st.markdown("---")
        if st.button("🔓 Logout", key="logout_3"):
            st.session_state.admin_logged_in = False
            st.rerun()