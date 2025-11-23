import streamlit as st
from src.parser import parse_resume
from src.skills import extract_skills
from src.scoring import full_score
from src.rewriter import rewrite_experience
from src.utils import extract_contact_info
import os

st.set_page_config(page_title="AI Resume Optimizer", layout="wide")

st.title("AI Resume Optimizer")

uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_desc = st.text_area("Paste the target job description (optional)")

if uploaded:
    os.makedirs("data/tmp", exist_ok=True)
    file_path = f"data/tmp/{uploaded.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded.getbuffer())

    text = parse_resume(file_path)

    st.subheader("📄 Extracted Resume Text (First 500 characters)")
    st.code(text[:500])

    st.subheader("📞 Contact Information")
    st.json(extract_contact_info(text))

    st.subheader("🧠 Detected Skills")
    skills = extract_skills(text)
    st.write(skills)

    st.subheader("📊 Resume Score")
    score = full_score(text, job_desc)
    st.json(score)

    st.subheader("✍️ Rewritten Experience Section")
    first_block = "\n".join(text.split("\n")[:5])
    rewritten = rewrite_experience(first_block, job_desc)
    st.text_area("Improved Version:", rewritten, height=200)
