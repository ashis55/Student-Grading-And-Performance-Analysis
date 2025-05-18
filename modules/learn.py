import fitz
import streamlit as st
import re
import fitz  # PyMuPDF
from docx import Document
from collections import Counter
import os
import base64
# Extract text from PDF

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

# Extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Resume Analyzer UI
def resume_analyzer_ui():
    st.subheader("📄 Resume Analyzer")

    uploaded_file = st.file_uploader("Upload your resume (PDF or Word)", type=["pdf", "docx"])
    
    if not uploaded_file:
        st.info("Please upload your resume to analyze.")
        return

    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == 'pdf':
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        return

    if not resume_text.strip():
        st.error("The file doesn't contain readable text. Please check your upload.")
        return

    required_skills = {
        "Software Engineer": ["Python", "Java", "C++", "Algorithms", "Data Structures", "Problem Solving", "Git"],
        "Data Scientist": ["Python", "R", "Machine Learning", "Deep Learning", "Statistics", "Data Analysis", "SQL", "TensorFlow"],
        "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB", "Git", "REST APIs"],
        "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "AI Algorithms", "Data Structures"]
    }

    total_possible_skills = sum(len(skills) for skills in required_skills.values())
    total_matched_skills = 0
    skill_match = {}
    skill_frequency = Counter()

    # Match skills and count
    for role, skills in required_skills.items():
        skill_count = 0
        for skill in skills:
            if re.search(r"\b" + re.escape(skill) + r"\b", resume_text, re.IGNORECASE):
                skill_count += 1
                skill_frequency[skill] += 1
        skill_match[role] = skill_count
        total_matched_skills += skill_count

    # Resume Score out of 100
    score_percentage = (total_matched_skills / total_possible_skills) * 100
    st.write(f"#### 📝 Resume Score: {score_percentage:.2f} / 100 (based on skill matches)")

    # Missing Skills
    st.write("#### ❌ Missing Skills:")
    for role, match in skill_match.items():
        missing_skills = [skill for skill in required_skills[role] if not re.search(r"\b" + re.escape(skill) + r"\b", resume_text, re.IGNORECASE)]
        if missing_skills:
            st.write(f"- **{role}:** {', '.join(missing_skills)}")

    # Role Fit Evaluation
    st.write("#### ✅ Role Fit Evaluation:")
    for role, match in skill_match.items():
        total_skills = len(required_skills[role])
        match_percentage = (match / total_skills) * 100
        st.write(f"- **{role}:** {match_percentage:.2f}% fit")

    # Strong Points
    st.write("#### 💪 Strong Points:")
    if skill_frequency:
        top_skills = [skill for skill, count in skill_frequency.items() if count >= 2]
        if top_skills:
            st.success(", ".join(top_skills))
        else:
            st.info("No standout strong points found across multiple roles.")

    # Weak Points
    st.write("#### ⚠️ Weak Points:")
    all_required = set(skill for skills in required_skills.values() for skill in skills)
    present_skills = set(skill_frequency.keys())
    missing = all_required - present_skills
    if missing:
        st.warning(", ".join(missing))
    else:
        st.success("Great! No missing critical skills across the roles.")

    # Suggestions
    st.write("#### 💡 Suggestions for Improvement:")
    for role, match in skill_match.items():
        if match < len(required_skills[role]):
            st.write(f"To improve your chances for **{role}**, consider adding the missing key skills.")

# def resume_analyzer_ui():
#     st.subheader("📄 Resume Analyzer")

#     uploaded_file = st.file_uploader("Upload your resume (PDF or Word)", type=["pdf", "docx"])
    
#     if not uploaded_file:
#         st.info("Please upload your resume to analyze.")
#         return

#     file_extension = uploaded_file.name.split('.')[-1].lower()

#     if file_extension == 'pdf':
#         resume_text = extract_text_from_pdf(uploaded_file)
#     elif file_extension == 'docx':
#         resume_text = extract_text_from_docx(uploaded_file)
#     else:
#         st.error("Unsupported file type. Please upload a PDF or DOCX file.")
#         return

#     if not resume_text.strip():
#         st.error("The file doesn't contain readable text. Please check your upload.")
#         return

#     required_skills = {
#         "Software Engineer": ["Python", "Java", "C++", "Algorithms", "Data Structures", "Problem Solving", "Git"],
#         "Data Scientist": ["Python", "R", "Machine Learning", "Deep Learning", "Statistics", "Data Analysis", "SQL", "TensorFlow"],
#         "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB", "Git", "REST APIs"],
#         "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "AI Algorithms", "Data Structures"]
#     }

#     score = 0
#     skill_match = {}
#     skill_frequency = Counter()

#     # Match skills and count
#     for role, skills in required_skills.items():
#         skill_count = 0
#         for skill in skills:
#             if re.search(r"\b" + re.escape(skill) + r"\b", resume_text, re.IGNORECASE):
#                 skill_count += 1
#                 skill_frequency[skill] += 1
#         skill_match[role] = skill_count
#         score += skill_count

#     st.write(f"#### 📝 Resume Score: {score} (based on skill matches)")

#     # Missing Skills
#     st.write("#### ❌ Missing Skills:")
#     for role, match in skill_match.items():
#         missing_skills = [skill for skill in required_skills[role] if skill.lower() not in resume_text.lower()]
#         if missing_skills:
#             st.write(f"- **{role}:** {', '.join(missing_skills)}")

#     # Role Fit Evaluation
#     st.write("#### ✅ Role Fit Evaluation:")
#     for role, match in skill_match.items():
#         total_skills = len(required_skills[role])
#         match_percentage = (match / total_skills) * 100
#         st.write(f"- **{role}:** {match_percentage:.2f}% fit")

#     # Strong & Weak Points
#     st.write("#### 💪 Strong Points:")
#     if skill_frequency:
#         top_skills = [skill for skill, count in skill_frequency.items() if count >= 2]
#         if top_skills:
#             st.success(", ".join(top_skills))
#         else:
#             st.info("No standout strong points found across multiple roles.")

#     st.write("#### ⚠️ Weak Points:")
#     all_required = set(skill for skills in required_skills.values() for skill in skills)
#     present_skills = set(skill_frequency.keys())
#     missing = all_required - present_skills
#     if missing:
#         st.warning(", ".join(missing))
#     else:
#         st.success("Great! No missing critical skills across the roles.")

#     # Suggestions
#     st.write("#### 💡 Suggestions for Improvement:")
#     for role, match in skill_match.items():
#         if match < len(required_skills[role]):
#             st.write(f"To improve your chances for **{role}**, consider adding the missing key skills.")


# --- Main UI Function ---
def learning_horizons_ui():
    st.subheader("🚀 Learning Horizons")

    tabs = st.tabs([  
        "📚 Recommended Courses", 
        "🧠 Career Quiz", 
        "📘 DSA & Competitive Programming",  
        "🎓 Scholarships & Exams", 
        "🚀 Skill Development Roadmap",
        "📄 Resume Analyzer" ,
         # Added tab for Resume Analyzer
    ])

    # --- Tab 1: Courses ---
    with tabs[0]:
        interests = st.multiselect("Select Interests", ["AI", "Web Development", "Data Science", "Cybersecurity", "Finance", "Marketing"])
        if interests:
            st.write("#### Suggested Courses:")
            for interest in interests:
                if interest == "AI":
                    st.markdown("""
                    - [Intro to AI (Coursera)](https://www.coursera.org/learn/introduction-to-ai)
                    - [AI for Everyone (Andrew Ng)](https://www.coursera.org/learn/ai-for-everyone)
                    - [Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning)
                    """)
                elif interest == "Web Development":
                    st.markdown("""
                    - [Full Stack Web Dev (freeCodeCamp)](https://www.freecodecamp.org/learn/)
                    - [Web Dev Bootcamp (Udemy)](https://www.udemy.com/course/the-web-developer-bootcamp/)
                    - [JavaScript.info](https://javascript.info/)
                    """)
                elif interest == "Data Science":
                    st.markdown("""
                    - [Data Science Specialization (Coursera)](https://www.coursera.org/specializations/jhu-data-science)
                    - [Python for Data Science (edX)](https://www.edx.org/course/python-for-data-science)
                    - [DataCamp Career Tracks](https://www.datacamp.com/)
                    """)
                elif interest == "Cybersecurity":
                    st.markdown("""
                    - [Intro to Cybersecurity (edX)](https://www.edx.org/course/introduction-to-cybersecurity)
                    - [Google Cybersecurity Professional Cert](https://www.coursera.org/professional-certificates/google-cybersecurity)
                    """)
                elif interest == "Finance":
                    st.markdown("""
                    - [Finance for Beginners (Coursera)](https://www.coursera.org/learn/financial-markets)
                    - [Investopedia Academy](https://www.investopedia.com/academy)
                    """)
                elif interest == "Marketing":
                    st.markdown("""
                    - [Digital Marketing Basics (Google)](https://learndigital.withgoogle.com/)
                    - [SEO Specialization (Coursera)](https://www.coursera.org/specializations/seo)
                    """)
        else:
            st.info("Select interests to see course suggestions.")

    # --- Tab 2: Career Quiz ---
    with tabs[1]:
        st.write("Find a suitable career based on your preferences.")
        total_score = 0
        q1 = st.radio("Do you enjoy logical thinking?", ["Yes", "Somewhat", "No"])
        total_score += {"Yes": 3, "Somewhat": 2, "No": 1}[q1]

        q2 = st.radio("Do you prefer working with code or visuals?", ["Code", "Visuals", "Both"])
        total_score += {"Code": 3, "Both": 2, "Visuals": 1}[q2]

        q3 = st.radio("Which environment suits you?", ["Structured", "Flexible", "Dynamic"])
        total_score += {"Structured": 3, "Dynamic": 2, "Flexible": 1}[q3]
          
        q4 = st.radio("Do you enjoy solving puzzles or complex problems?", ["Yes", "Sometimes", "Rarely"])
        total_score += {"Yes": 3, "Sometimes": 2, "Rarely": 1}[q4]

        q5 = st.radio("How comfortable are you with public interaction?", ["Very comfortable", "Somewhat", "Not at all"])
        total_score += {"Not at all": 3, "Somewhat": 2, "Very comfortable": 1}[q5]

        if st.button("🎯 Get Career Suggestion"):
            if total_score >= 13:
                st.success("💼 You might enjoy **Software Engineering**, **AI**, or **Data Science**.")
            elif 5 <= total_score < 13:
                st.success("📊 You might enjoy **UI/UX**, **Product Design**, or **Marketing**.")
            else:
                st.success("🔧 Consider exploring **Support Roles**, **Content Creation**, or **Teaching**.")

    # --- Tab 3: DSA & CP ---
    with tabs[2]:
        st.markdown("### 📘 DSA Resources")
        st.markdown("""- [DSA on LeetCode](https://leetcode.com/explore/)
- [GeeksforGeeks DSA Course](https://practice.geeksforgeeks.org/courses/dsa-self-paced)
- [Striver's DSA Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)""")

        st.markdown("### ⚔️ Competitive Programming Platforms")
        st.markdown("""- [Codeforces](https://codeforces.com/)
- [AtCoder](https://atcoder.jp/)
- [CodeChef](https://www.codechef.com/)
- [CSES Problem Set](https://cses.fi/problemset/)
- [A2OJ Ladders](https://a2oj.com/Ladders)""")

        # rating = st.slider("Rate your CP comfort level (0 = beginner, 100 = expert)", 0, 100, 50)
        # if rating < 30:
        #     st.info("💡 Start with beginner problems on LeetCode or Codeforces Div 3.")
        # elif rating < 70:
        #     st.success("🔥 Practice contests weekly on Codeforces/CodeChef.")
        # else:
        #     st.balloons()
        #     st.success("🏆 You're ready for Div 1 and global competitions!")

    # --- Tab 4: Scholarships ---
    with tabs[3]:
        exam_data = {
            "GATE": "https://gate.iitkgp.ac.in/",
            "GRE": "https://www.ets.org/gre",
            "TOEFL": "https://www.ets.org/toefl",
            "IELTS": "https://www.ielts.org/",
            "Scholarship Portal (India)": "https://scholarships.gov.in/",
            "Commonwealth Scholarships": "https://cscuk.fcdo.gov.uk/",
            "DAAD Germany": "https://www.daad.de/en/",
            "TCS NQT": "https://learning.tcsionhub.in/hub/nqt/",
            "Infosys Springboard": "https://infyspringboard.onwingspan.com/"
        }
        for k, v in exam_data.items():
            st.markdown(f"- [{k}]({v})")

    # --- Tab 5: Skill Development Roadmap ---
    with tabs[4]:
        career_paths = {
            "AI Engineer": [
                "📚 Learn foundational Math (Linear Algebra, Probability, Statistics)",
                "👨‍💻 Master Python programming (NumPy, Pandas, Matplotlib)",
                "🧠 Study Machine Learning (Supervised/Unsupervised, Scikit-learn)",
                "🧾 Work on real AI projects (chatbots, image recognition, etc.)",
                "🧪 Try deep learning (TensorFlow, PyTorch)"
            ],
            "Web Developer": [
                "🛠 Learn HTML, CSS, JavaScript fundamentals",
                "🎨 Build UI using frameworks like React or Vue.js",
                "🌐 Master backend (Node.js, Express, or Django)",
                "🗃 Learn about databases (SQL, MongoDB)",
                "🚀 Deploy full-stack apps using platforms like Vercel or Heroku"
            ],
            "Data Analyst": [
                "📊 Master Excel and data visualization",
                "🔍 Learn SQL for data queries",
                "👨‍💻 Learn Python (Pandas, Matplotlib, Seaborn)",
                "📈 Practice with datasets on Kaggle",
                "🧾 Create dashboards using Power BI or Tableau"
            ],
            "Cybersecurity Analyst": [
                "🔐 Learn fundamentals of network & system security",
                "👨‍💻 Understand Linux, command line, and system tools",
                "🕵️‍♂️ Study ethical hacking and penetration testing",
                "🧠 Learn about firewalls, IDS/IPS, and encryption",
                "🎓 Earn certifications (e.g., CompTIA Security+, CEH)"
            ],
            "Cloud Engineer": [
                "☁️ Learn core cloud concepts (IaaS, PaaS, SaaS)",
                "👨‍💻 Get hands-on with AWS, Azure, or GCP",
                "🛠 Study containerization (Docker, Kubernetes)",
                "📦 Understand DevOps pipelines (CI/CD, Jenkins)",
                "🎓 Consider cloud certs (AWS Associate, Azure Fundamentals)"
            ],
            "Mobile App Developer": [
                "📱 Learn native development (Kotlin for Android, Swift for iOS)",
                "🔁 Or learn cross-platform tools (Flutter, React Native)",
                "🧱 Build UI and manage state effectively",
                "🗃 Connect apps to cloud or database (Firebase)",
                "🚀 Publish apps to Play Store or App Store"
            ]
        }

        career_choice = st.selectbox("🎯 Choose a Career Path", list(career_paths.keys()))
        if career_choice:
            st.markdown(f"#### 📘 Roadmap for **{career_choice}**")
            for step in career_paths[career_choice]:
                st.write(f"- {step}")
    
    with tabs[5]:
        resume_analyzer_ui()
    
    # with tabs[5]:
    #  ebooks_ui()