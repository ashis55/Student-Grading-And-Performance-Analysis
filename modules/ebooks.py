
# import streamlit as st
# import os
# import base64
# import time
# import pandas as pd
# import json

# # Load or Save descriptions
# def load_descriptions(category_path):
#     desc_path = os.path.join(category_path, "descriptions.json")
#     if os.path.exists(desc_path):
#         with open(desc_path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     return {}

# def save_descriptions(category_path, descriptions):
#     desc_path = os.path.join(category_path, "descriptions.json")
#     with open(desc_path, "w", encoding="utf-8") as f:
#         json.dump(descriptions, f, indent=4)

# # PDF viewer
# def show_pdf_viewer(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode("utf-8")
#         pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
#         st.markdown(pdf_display, unsafe_allow_html=True)

# # Login form
# def login_form(student_df):
#     st.title("📚 Ebook Management")
#     user_id = st.text_input("Enter ID")
#     password = st.text_input("Enter Password", type="password")
#     login_as = st.selectbox("Role", ["Admin", "Student"])

#     if st.button("Login"):
#         if login_as == "Admin":
#             if (user_id == "admin001" and password == "admin@123") or (user_id == "admin002" and password == "admin@456"):
#                 st.session_state.logged_in = True
#                 st.session_state.user_role = "Admin"
#                 st.session_state.user_id = user_id
#                 st.query_params = {"logged_in": ["true"], "role": ["admin"]}
#                 st.rerun()
#             else:
#                 st.error("Invalid Admin credentials")
#         else:
#             matched = student_df[
#                 (student_df["ID"].astype(str) == str(user_id)) & 
#                 (student_df["Password"].astype(str) == str(password))
#             ]
#             if not matched.empty:
#                 st.session_state.logged_in = True
#                 st.session_state.user_role = "Student"
#                 st.session_state.user_id = user_id
#                 st.query_params = {"logged_in": ["true"], "role": ["student"], "user_id": [str(user_id)]}
#                 st.rerun()
#             else:
#                 st.error("Invalid Student credentials")

# # Main UI
# def ebooks_ui():
#     try:
#         student_df = pd.read_excel("data/student_data.xlsx", engine="openpyxl")
#     except Exception as e:
#         st.error(f"Error loading student data: {e}")
#         st.stop()

#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False
#         st.session_state.user_role = None
#         st.session_state.user_id = None

#     if not st.session_state.logged_in:
#         login_form(student_df)
#         return

#     base_dir = "ebooks"
#     os.makedirs(base_dir, exist_ok=True)
#     categories = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

#     # Admin View
#     if st.session_state.user_role == "Admin":
#         st.title("📘 Ebooks Library - Admin Panel")
#         selected_category = st.selectbox("Select Category", categories) if categories else None

#         st.subheader("Upload New Book")
#         new_category = st.text_input("Enter category (existing or new)")
#         book_name = st.text_input("Enter Book Name (with .pdf extension)")
#         description = st.text_area("Enter Book Description")
#         uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

#         if st.button("Upload Book"):
#             if not new_category or not book_name or not uploaded_file:
#                 st.warning("Please fill all fields and select a file.")
#             else:
#                 category_path = os.path.join(base_dir, new_category)
#                 os.makedirs(category_path, exist_ok=True)
#                 save_path = os.path.join(category_path, book_name)
#                 with open(save_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())

#                 descriptions = load_descriptions(category_path)
#                 descriptions[book_name] = description
#                 save_descriptions(category_path, descriptions)

#                 st.success(f"Book '{book_name}' uploaded with description.")
#                 st.rerun()

#         # List books
#         if selected_category:
#             st.subheader(f"Books in '{selected_category}'")
#             category_path = os.path.join(base_dir, selected_category)
#             books = [b for b in os.listdir(category_path) if b.lower().endswith(".pdf")]
#             descriptions = load_descriptions(category_path)

#             for book in books:
#                 book_path = os.path.join(category_path, book)
#                 cols = st.columns([3, 1, 1])
#                 with cols[0]:
#                     st.write(f"**{book}**")
#                     st.write(f"*Description:* {descriptions.get(book, 'No description available.')}")
#                 with cols[1]:
#                     if st.button(f"View {book}", key=f"view_{book}"):
#                         show_pdf_viewer(book_path)
#                 with cols[2]:
#                     with open(book_path, "rb") as f:
#                         st.download_button(f"Download {book}", f, book, mime="application/pdf", key=f"download_{book}")

#         if st.button("Logout"):
#             st.session_state.pop("logged_in", None)
#             st.session_state.pop("user_role", None)
#             st.session_state.pop("user_id", None)
#             st.query_params = {}
#             st.rerun()

#     # Student View
#     elif st.session_state.user_role == "Student":
#         st.title("📘 Ebooks Library - Student Panel")
#         if not categories:
#             st.info("No categories found.")
#             return

#         selected_category = st.selectbox("Select Category", categories)
#         category_path = os.path.join(base_dir, selected_category)
#         books = [b for b in os.listdir(category_path) if b.lower().endswith(".pdf")]
#         descriptions = load_descriptions(category_path)

#         for book in books:
#             book_path = os.path.join(category_path, book)
#             cols = st.columns([3, 1])
#             with cols[0]:
#                 st.write(f"**{book}**")
#                 st.write(f"*Description:* {descriptions.get(book, 'No description available.')}")
#             with cols[1]:
#                 if st.button(f"View {book}", key=f"view_{book}"):
#                     show_pdf_viewer(book_path)
#                 with open(book_path, "rb") as f:
#                     st.download_button(f"Download {book}", f, book, mime="application/pdf", key=f"download_{book}")

#         if st.button("Logout"):
#          st.session_state.pop("logged_in", None)
#          st.session_state.pop("user_role", None)
#          st.session_state.pop("user_id", None)
#          st.query_params = {}
#          st.rerun()

# if __name__ == "__main__":
#     ebooks_ui()



import streamlit as st
import os
import base64
import time
import pandas as pd
import json

# PDF Viewer using base64 embedding
def show_pdf_viewer(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

# Load or save descriptions
def load_descriptions(category_path):
    desc_path = os.path.join(category_path, "descriptions.json")
    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_descriptions(category_path, descriptions):
    desc_path = os.path.join(category_path, "descriptions.json")
    with open(desc_path, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, indent=4)

# Login form
def login_form(student_df):
    st.title("📚 Ebook Management")
    user_id = st.text_input("Enter ID")
    password = st.text_input("Enter Password", type="password")
    login_as = st.selectbox("Role", ["Admin", "Student"])

    if st.button("Login"):
        if login_as == "Admin":
            if (user_id == "admin001" and password == "admin@123") or (user_id == "admin002" and password == "admin@456"):
                st.session_state.logged_in = True
                st.session_state.user_role = "Admin"
                st.session_state.user_id = user_id
                st.query_params = {"logged_in": ["true"], "role": ["admin"]}
                st.rerun()
            else:
                st.error("Invalid Admin credentials")
        else:
            matched = student_df[
                (student_df["ID"].astype(str) == str(user_id)) & 
                (student_df["Password"].astype(str) == str(password))
            ]
            if not matched.empty:
                st.session_state.logged_in = True
                st.session_state.user_role = "Student"
                st.session_state.user_id = user_id
                st.query_params = {"logged_in": ["true"], "role": ["student"], "user_id": [str(user_id)]}
                st.rerun()
            else:
                st.error("Invalid Student credentials")

# Main UI
def ebooks_ui():
    try:
        student_df = pd.read_excel("data/student_data.xlsx", engine="openpyxl")
    except Exception as e:
        st.error(f"Error loading student data: {e}")
        st.stop()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_id = None

    if not st.session_state.logged_in:
        login_form(student_df)
        return

    base_dir = "ebooks"
    os.makedirs(base_dir, exist_ok=True)
    categories = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    # Admin View
    if st.session_state.user_role == "Admin":
        st.title("📘 Ebooks Library - Admin Panel")
        selected_category = st.selectbox("Select Category", categories) if categories else None

        st.subheader("Upload New Book")
        new_category = st.text_input("Enter category (existing or new)")
        book_name = st.text_input("Enter Book Name (with .pdf extension)")
        description = st.text_area("Enter Book Description")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if st.button("Upload Book"):
            if not new_category or not book_name or not uploaded_file:
                st.warning("Please fill all fields and select a file.")
            else:
                category_path = os.path.join(base_dir, new_category)
                os.makedirs(category_path, exist_ok=True)
                save_path = os.path.join(category_path, book_name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                descriptions = load_descriptions(category_path)
                descriptions[book_name] = description
                save_descriptions(category_path, descriptions)

                st.success(f"Book '{book_name}' uploaded with description.")
                st.rerun()

        if selected_category:
            st.subheader(f"Books in '{selected_category}'")
            category_path = os.path.join(base_dir, selected_category)
            books = [b for b in os.listdir(category_path) if b.lower().endswith(".pdf")]
            descriptions = load_descriptions(category_path)

            for book in books:
                book_path = os.path.join(category_path, book)
                st.markdown("----")
                cols = st.columns([4, 1])
                with cols[0]:
                    st.write(f"### 📖 {book}")
                    st.write(f"**Description:** {descriptions.get(book, 'No description available.')}")

                    with st.expander("🔍 Preview Book"):
                        show_pdf_viewer(book_path)

                with cols[1]:
                    with open(book_path, "rb") as f:
                        st.download_button(f"⬇️ Download", f, book, mime="application/pdf", key=f"download_{book}")

        if st.button("Logout"):
            st.session_state.clear()
            st.query_params = {}
            st.rerun()

    # Student View
    elif st.session_state.user_role == "Student":
        st.title("📘 Ebooks Library - Student Panel")
        if not categories:
            st.info("No categories found.")
            return

        selected_category = st.selectbox("Select Category", categories)
        category_path = os.path.join(base_dir, selected_category)
        books = [b for b in os.listdir(category_path) if b.lower().endswith(".pdf")]
        descriptions = load_descriptions(category_path)

        for book in books:
            book_path = os.path.join(category_path, book)
            st.markdown("----")
            cols = st.columns([4, 1])
            with cols[0]:
                st.write(f"### 📖 {book}")
                st.write(f"**Description:** {descriptions.get(book, 'No description available.')}")

                with st.expander("🔍 Preview Book"):
                    show_pdf_viewer(book_path)

            with cols[1]:
                with open(book_path, "rb") as f:
                    st.download_button(f"⬇️ Download", f, book, mime="application/pdf", key=f"download_{book}")

        if st.button("Logout"):
            st.session_state.clear()
            st.query_params = {}
            st.rerun()

if __name__ == "__main__":
    ebooks_ui()
