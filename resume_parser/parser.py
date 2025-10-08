# resume_parser/parser.py
import re
from pathlib import Path
from io import BytesIO

# PDF text extraction dependency
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

# spaCy optional (best effort). If not available, fallback to keyword matching.
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except Exception:
    spacy = None
    nlp = None

# A reasonable skill vocabulary to fallback on (lowercase)
FALLBACK_SKILLS = [
    "python","java","c++","c","javascript","html","css","react","nodejs","node",
    "sql","postgresql","mysql","mongodb","pandas","numpy","scikit-learn","tensorflow",
    "pytorch","keras","docker","kubernetes","aws","azure","gcp","git","linux",
    "streamlit","flask","django","nlp","spaCy","opencv","matlab","excel"
]

EDU_KEYWORDS = ["btech","bachelor","master","m.tech","mtech","b.sc","msc","diploma","cgpa","degree","college","university"]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def _read_pdf_bytes(file_like):
    """Return extracted text from a file-like object or a path (best-effort)."""
    text = ""
    if PdfReader is None:
        raise RuntimeError("PyPDF2 is required. Install with: pip install PyPDF2")
    # file_like may be a path string, Path, bytes, or file-like with read()
    if isinstance(file_like, (str, Path)):
        path = Path(file_like)
        with open(path, "rb") as f:
            reader = PdfReader(f)
            for p in reader.pages:
                try:
                    text += p.extract_text() or ""
                except Exception:
                    continue
    else:
        # assume file-like or bytes
        if hasattr(file_like, "read"):
            raw = file_like.read()
        elif isinstance(file_like, (bytes, bytearray)):
            raw = bytes(file_like)
        else:
            raw = None
        if raw is None:
            return ""
        stream = BytesIO(raw)
        reader = PdfReader(stream)
        for p in reader.pages:
            try:
                text += p.extract_text() or ""
            except Exception:
                continue
    return text

def extract_email(text):
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None

def extract_education(text):
    edu_lines = []
    for line in text.splitlines():
        low = line.strip().lower()
        for kw in EDU_KEYWORDS:
            if kw in low:
                cleaned = " ".join(line.strip().split())
                edu_lines.append(cleaned)
                break
    # Deduplicate and return
    return list(dict.fromkeys(edu_lines))[:6]

def extract_skills_spacy(text):
    """Use spaCy to find noun chunks / tokens matching skill vocab (if model available)."""
    if nlp is None:
        return []
    doc = nlp(text)
    found = set()
    # use named entities and noun tokens
    for ent in doc.ents:
        found.add(ent.text.lower())
    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and len(token.text) <= 30:
            found.add(token.text.lower())
    # filter by fallback vocab
    return sorted({s for s in found if any(k in s for k in FALLBACK_SKILLS)})

def extract_skills_fallback(text):
    found = set()
    lowered = text.lower()
    for skill in FALLBACK_SKILLS:
        # word boundary match
        if re.search(rf"\b{re.escape(skill)}\b", lowered):
            found.add(skill)
    return sorted(found)

def parse_resume(file_input):
    """
    Parses a resume (file path or file-like object) and returns a dict:
    {
      "skills": [...],
      "education": [...],
      "email": "a@b.com",
      "raw_text": "...."
    }
    """
    # Read text
    try:
        text = _read_pdf_bytes(file_input)
    except Exception as e:
        # If PDF reader fails, try treating input as plain text
        try:
            if hasattr(file_input, "read"):
                text = file_input.read().decode(errors="ignore")
            elif isinstance(file_input, (bytes, bytearray)):
                text = file_input.decode(errors="ignore")
            else:
                text = str(file_input)
        except Exception:
            text = ""
    text = text or ""

    # Extract email
    email = extract_email(text)

    # Extract education
    education = extract_education(text)

    # Extract skills: prefer spaCy-based if available, otherwise fallback
    skills = []
    try:
        if nlp:
            skills = extract_skills_spacy(text)
        if not skills:
            skills = extract_skills_fallback(text)
    except Exception:
        skills = extract_skills_fallback(text)

    # Clean skills formatting (unique, title-case)
    skills = [s.strip() for s in skills if s.strip()]
    skills = list(dict.fromkeys(skills))  # preserve order, dedupe

    return {
        "skills": skills,
        "education": education,
        "email": email,
        "raw_text": text[:4000]  # preview
    }
