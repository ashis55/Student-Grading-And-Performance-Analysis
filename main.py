import streamlit as st
import pandas as pd
import os

# Import Student Functions from modules
from modules.student import student_login, student_dashboard

# --- Page Config ---
st.set_page_config(page_title="Student Academic Performance Portal", layout="wide")

# --- Sidebar ---

with st.sidebar:
    st.markdown("""
        <style>
          .sidebar-title {
    font-size: 18px;
    font-weight: 600;
    color: white;
    background-color: #4B8BBE;  /* Python blue */
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: inline-block;
}

            .sidebar-radio label {
                font-size: 16px !important;
                font-weight: 500;
                padding: 6px 14px;
                border-radius: 10px;
                display: block;
                transition: 0.3s;
            }
            .sidebar-radio label:hover {
                background-color: #f0f2f6;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title">🎯 Navigation</div>', unsafe_allow_html=True)

    navigation_options = [
        "🏠 Home",
        "🎓 Student Dashboard",
        "🛡️ Admin Dashboard",
        "📊 Performance Trend Module",
        "🎓 Career & Learning",
        "📚 Ebooks",
    ]

    selected_option = st.radio(
        " ", navigation_options, label_visibility="collapsed", key="sidebar_radio"
    )

# --- Load Student Data ---
@st.cache_data
def load_student_data():
    try:
        return pd.read_excel(os.path.join("data", "student_data.xlsx"), engine="openpyxl")
    except Exception as e:
        st.error(f"Error loading student data: {e}")
        st.stop()

df = load_student_data()

# --- Initialize Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'student_data' not in st.session_state:
    st.session_state.student_data = None

# --- Home Page ---
def show_home():
    st.title("🎓  University")
    st.subheader("Student Grade and Performance Analysis System")

    col1, col2 = st.columns(2)

    with col1:
        st.image("assets/b1.jpg", use_container_width=True, caption="Welcome to the Student Portal")
      
    with col2:
        st.markdown("### 📢 Latest Announcements")
        try:
            notice_df = pd.read_excel("data/notices.xlsx", engine="openpyxl")
            for _, row in notice_df.iterrows():
                with st.expander(f"📌 {row['title']} ({row['date'].strftime('%d/%m/%Y')})"):
                    st.write(row['description'])
        except Exception as e:
            st.warning("No notices available or failed to load notice board.")

    st.markdown("### 📰 News & Events")
    try:
        news_df = pd.read_excel("data/news_events.xlsx", engine="openpyxl")
        for _, row in news_df.iterrows():
            with st.expander(f"📰 {row['title']} ({row['date'].strftime('%d/%m/%Y')})"):
                st.write(row['description'])
    except Exception as e:
        st.warning("No news available or failed to load news feed.")

def department_analytics_dashboard():
    st.title("💼 Placement Dashboard")
    st.info("Placement Dashboard is under development 🚧")


def future_education():
    st.title("🎯 Future Education")
    st.info("Future Education section is under development 🚧")

# --- Routing ---
if selected_option == "🏠 Home":
    show_home()
elif selected_option == "🎓 Student Dashboard":
    if not st.session_state.logged_in:
        student_login(df)
    else:
        student_dashboard(st.session_state.student_data, df)
elif selected_option == "🛡️ Admin Dashboard":
    from modules.admin import admin_dashboard
    admin_dashboard()
# elif selected_option == "📊 Department Analytics":
#     from modules.performance_trends import department_analytics_dashboard
#     department_analytics_dashboard(df)
elif selected_option == "📊 Performance Trend Module":
    from modules.performance_trends import department_analytics_dashboard
    department_analytics_dashboard(df)


elif selected_option.strip() == "🎓 Career & Learning":
    from modules.learn import learning_horizons_ui
    learning_horizons_ui()


elif selected_option == "📚 Ebooks":
    from modules.ebooks import ebooks_ui
    ebooks_ui()



