import streamlit as st
from resume_parser.parser import parse_resume
from quiz.quiz_engine import get_quiz_questions, evaluate_answers
from recommender.engine import recommend_roles

st.set_page_config(page_title="Smart Career Counselor Agent", layout="centered")

st.title("🎓 Smart Career Counselor Agent")

# Step 1: Upload Resume
st.header("📄 Upload Your Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

user_skills = []
education = []
if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())
    result = parse_resume("temp_resume.pdf")
    user_skills = result["skills"]
    education = result["education"]

    st.subheader("Extracted Skills")
    st.write(", ".join(user_skills) if user_skills else "No skills found")

    st.subheader("Education Info")
    st.write("\n".join(education) if education else "No education info found")

# Step 2: Career Quiz
st.header("🧠 Career Interest Quiz")

if 'answers' not in st.session_state:
    st.session_state.answers = []

questions = get_quiz_questions()
for i, q in enumerate(questions):
    response = st.radio(q["question"], ["Yes", "No"], key=f"quiz_{i}")
    if response == "Yes":
        st.session_state.answers.append(q["field"])

# Step 3: Recommendations
if st.button("🎯 Get Career Recommendations"):
    if not user_skills:
        st.error("Please upload a resume first.")
    elif not st.session_state.answers:
        st.error("Please answer the quiz.")
    else:
        interest_field = evaluate_answers(st.session_state.answers)
        recommendations = recommend_roles(user_skills, interest_field)

        st.header("📌 Recommended Career Paths")
        for rec in recommendations:
            st.subheader(rec["title"])
            st.write(f"✅ Skill Match Score: {rec['match_count']}")
            st.markdown("**Recommended Courses:**")
            for course in rec["recommended_courses"]:
                st.write(f"- {course}")
