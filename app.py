import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="AI Resume Reviewer", page_icon="📝")

def extract_text_from_pdf(uploaded):
    text = ""
    with pdfplumber.open(uploaded) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            text += "\n" + t
    return text

ROLE_KEYWORDS = {
    "data analyst": {"excel","sql","power bi","tableau","dashboard","python","statistics"},
    "data scientist": {"python","ml","machine learning","classification","regression","pandas","numpy","tensorflow"},
    "product manager": {"roadmap","stakeholders","user stories","kpi","jira","agile","scrum"},
}

st.title("📝 AI Resume Reviewer")

job_role = st.text_input("🎯 Enter Target Job Role", placeholder="e.g., Data Analyst")
mode = st.radio("Resume Input", ["Upload PDF", "Paste Text"])
resume_text = ""

if mode == "Upload PDF":
    up = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    if up is not None:
        resume_text = extract_text_from_pdf(up)
else:
    resume_text = st.text_area("Paste Resume Text", height=200)

if st.button("🔍 Review Resume"):
    if not resume_text.strip():
        st.warning("Please provide resume text.")
    elif not job_role.strip():
        st.warning("Please enter job role.")
    else:
        role = job_role.lower()
        kws = ROLE_KEYWORDS.get(role, set())
        found = {kw for kw in kws if kw in resume_text.lower()}
        missing = kws - found

        st.subheader("✅ Strengths")
        st.write(", ".join(found) if found else "No keywords found.")

        st.subheader("⚠️ Gaps")
        st.write(", ".join(missing) if missing else "Good coverage!")

        st.subheader("🛠 Suggestions")
        st.markdown("""
        - Add more measurable achievements (numbers, %).  
        - Use action words like *Developed, Led, Improved*.  
        - Keep resume 1–2 pages.  
        """)
