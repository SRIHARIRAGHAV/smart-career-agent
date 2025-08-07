import streamlit as st
from resume_parser.parser import parse_resume

st.title("🧠 Smart Career Counselor Agent")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")
    parsed_data = parse_resume(uploaded_file)

    st.subheader("📄 Extracted Resume Info")
    
    if parsed_data:
        st.write(f"**Name:** {parsed_data.get('name', 'N/A')}")
        st.write(f"**Email:** {parsed_data.get('email', 'N/A')}")
        
        # ✅ Show extracted skills
        skills = parsed_data.get('skills', [])
        if skills:
            st.write("**Skills:**")
            st.write(", ".join(skills))
        else:
            st.warning("No skills found in resume.")

        # You can also display education and experience similarly
