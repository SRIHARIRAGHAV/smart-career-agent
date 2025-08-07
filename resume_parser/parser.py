import re
import spacy
import pdfminer.high_level
from io import StringIO

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    output = StringIO()
    with open(pdf_path, 'rb') as f:
        text = pdfminer.high_level.extract_text(f)
    return text

def extract_skills(text):
    doc = nlp(text)
    skills = []
    for token in doc:
        if token.pos_ == "NOUN" and token.text.lower() in ["python", "java", "sql", "tensorflow", "react"]:
            skills.append(token.text)
    return list(set(skills))

def extract_education(text):
    education_keywords = ["Bachelor", "B.Tech", "M.Tech", "Master", "BSc", "MSc"]
    education = []
    for line in text.split('\n'):
        for keyword in education_keywords:
            if keyword in line:
                education.append(line.strip())
    return education

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(text)
    education = extract_education(text)
    return {
        "skills": skills,
        "education": education,
        "raw_text": text[:500]  # preview
    }
