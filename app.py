import streamlit as st
import PyPDF2
import docx
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Skills Database
SKILLS_DB = [
    "python", "java", "c++", "machine learning", "deep learning", "nlp",
    "data analysis", "sql", "html", "css", "javascript", "react", "django",
    "flask", "pandas", "numpy", "excel", "communication", "leadership",
    "problem-solving", "project management", "adaptability"
]

# --- Functions ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return "".join(page.extract_text() or "" for page in pdf_reader.pages)

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return " ".join([para.text for para in doc.paragraphs])

def extract_skills(text):
    text = text.lower()
    skills_found = []
    for skill in SKILLS_DB:
        if skill.lower() in text:
            skills_found.append(skill.capitalize())
    return list(set(skills_found))

def calculate_fit_score(resume_skills, job_skills):
    matches = set(resume_skills) & set(job_skills)
    score = (len(matches) / len(job_skills)) * 100 if job_skills else 0
    return round(score, 2), matches

def generate_suggestions(missing_skills):
    if not missing_skills:
        return "Your resume aligns well with the job description. No major changes needed."
    return (
        f"Consider adding these skills to your resume if you have experience in them: "
        f"{', '.join(missing_skills)}. "
        "You can include them in your project descriptions, skills section, or achievements."
    )

def display_skill_badges(skills, bg_color, text_color):
    """Display skills as colored badges in one or two lines using flexbox."""
    if skills:
        skill_html = "".join([
            f"""
            <span style='background-color:{bg_color};
                        color:{text_color};
                        padding:8px 12px;
                        border-radius:20px;
                        margin:4px;
                        display:inline-block;
                        font-weight:500;
                        white-space:nowrap;
                        box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
                        transition: all 0.3s ease;'>
                {skill}
            </span>
            """
            for skill in skills
        ])
        st.markdown(
            f"""
            <div style='display:flex; flex-wrap:wrap; gap:6px;'>
                {skill_html}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("None")

# --- Streamlit Layout ---
st.set_page_config(page_title="Skillfy Resume Analyzer", page_icon="📄", layout="wide")

# Main Title
st.markdown("<h1 style='text-align:center; color:#4CAF50;'>📄 Skillfy Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Analyze your resume against a job description to find skill matches and improvement suggestions.</p>", unsafe_allow_html=True)
st.markdown("---")

# Upload + Job Description
col1, col2 = st.columns([1, 1])
with col1:
    resume_file = st.file_uploader("📂 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
with col2:
    job_desc = st.text_area("📝 Paste Job Description", height=200)

# Submit Button
if st.button("Analyze Resume", use_container_width=True):
    if resume_file and job_desc:
        # Extract text from resume
        if resume_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        # Extract skills
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)

        # Calculate fit score
        score, matching_skills = calculate_fit_score(resume_skills, job_skills)
        missing_skills = set(job_skills) - set(resume_skills)

        # Display results in cards
        colA, colB = st.columns(2)
        with colA:
            st.markdown(
                f"<div style='background-color:#E8F5E9; padding:20px; border-radius:10px; text-align:center;'>"
                f"<h3 style='color:#2E7D32;'>Fit Score</h3><h1 style='color:#1B5E20;'>{score}%</h1></div>",
                unsafe_allow_html=True
            )
        with colB:
            st.markdown(
                f"<div style='background-color:#E3F2FD; padding:20px; border-radius:10px; text-align:center;'>"
                f"<h3 style='color:#1565C0;'>Total Matching Skills</h3><h1 style='color:#0D47A1;'>{len(matching_skills)}</h1></div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### ✅ Matching Skills", unsafe_allow_html=True)
        display_skill_badges(matching_skills, "#4CAF50", "white")

        st.markdown("### ❌ Missing Skills", unsafe_allow_html=True)
        display_skill_badges(missing_skills, "#FF5252", "white")

        st.markdown("### 💡 Resume Improvement Suggestions")
        st.info(generate_suggestions(missing_skills))

    else:
        st.warning("Please upload a resume and enter a job description before analyzing.")
