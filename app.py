import streamlit as st
from resume_parser.parser import parse_resume

st.title("🧠 Smart Career Counselor Agent")

uploaded_file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
if uploaded_file is not None:
    # pass the uploaded_file directly (it is file-like)
    parsed = parse_resume(uploaded_file)
    st.subheader("Extracted skills")
    st.write(parsed["skills"] or "No skills found")
    st.subheader("Education")
    st.write(parsed["education"] or "No education info found")
    st.subheader("Email")
    st.write(parsed["email"] or "No email found")
