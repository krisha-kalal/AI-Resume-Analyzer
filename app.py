import json
import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Custom CSS for Dark Glassmorphism Theme
st.markdown("""
<style>
    /* Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    /* Glassmorphism Cards */
    div[data-testid="stMetricValue"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    /* Primary Action Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Load Skill Mapping Database
@st.cache_data
def load_skill_db():
  try:
    with open("skills_db.json", "r") as f:
      return json.load(f)
  except FileNotFoundError:
    return {}


skills_db = load_skill_db()

# Extraction Helpers
def extract_text_from_pdf(pdf_file):
  text = ""
  with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
      extracted = page.extract_text()
      if extracted:
        text += extracted + "\n"
  return text


def extract_skills(text):
  extracted = []
  text_lower = text.lower()
  known_skills = [
      "python",
      "react",
      "java",
      "c++",
      "machine learning",
      "sql",
      "docker",
      "node.js",
      "html",
      "css",
      "javascript",
      "nlp",
      "express.js",
  ]
  for skill in known_skills:
    if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
      extracted.append(skill)
  return list(set(extracted))


def extract_education(text):
  degrees = ["b.tech", "b.e.", "b.sc", "m.tech", "m.sc", "bca", "mca", "phd"]
  for degree in degrees:
    if degree in text.lower():
      return degree.upper()
  return "Bachelor Degree (General)"


def extract_experience_years(text):
  matches = re.findall(
      r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience",
      text,
      re.IGNORECASE,
  )
  if matches:
    return max([int(m) for m in matches])
  return 1


# UI Layout
st.title("🤖 AI Resume Analyzer: Smart Resume Screening & Job Matcher")
st.caption("Silver Oak University | Department of Computer Engineering")

col1, col2 = st.columns(2)

with col1:
  st.subheader("1. Candidate Resume")
  uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

with col2:
  st.subheader("2. Job Description")
  job_description = st.text_area(
      "Paste Job Description Here",
      height=200,
      placeholder=(
          "Target Role: Full Stack / Machine Learning Engineer\nRequired"
          " Skills: Python, React, Machine Learning, SQL, Docker..."
      ),
  )

if st.button("Analyze & Evaluate Match", type="primary"):
  if uploaded_file is None or not job_description.strip():
    st.error(
        "Please upload a PDF resume and provide a job description to proceed."
    )
  else:
    with st.spinner("Parsing resume text and executing NLP scoring..."):
      resume_text = extract_text_from_pdf(uploaded_file)

      # Extract Fields
      resume_skills = extract_skills(resume_text)
      jd_skills = extract_skills(job_description)
      resume_edu = extract_education(resume_text)
      resume_exp = extract_experience_years(resume_text)

      # 1. Hard Skills Match Score (50%)
      vectorizer = TfidfVectorizer()
      tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
      skills_similarity = float(
          cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
      )
      skills_score = round(skills_similarity * 100, 2)

      # 2. Experience Fit Score (30%)
      exp_score = min(100.0, float(resume_exp * 25))

      # 3. Education Alignment Score (20%)
      edu_score = 90.0 if "b.tech" in resume_text.lower() else 75.0

      # Weighted Multi-Factor Formula (50% / 30% / 20%)
      total_score = round(
          (0.50 * skills_score) + (0.30 * exp_score) + (0.20 * edu_score), 2
      )

      # Skill Gaps
      missing_skills = [s for s in jd_skills if s not in resume_skills]

    st.success("Analysis Complete!")

    # Display Multi-Factor Sub-Scores
    st.subheader("📊 Multi-Factor Evaluation Results")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Overall Match Score", f"{total_score}%")
    m2.metric("Hard Skills Match (50%)", f"{skills_score}%")
    m3.metric("Experience Fit (30%)", f"{exp_score}%")
    m4.metric("Education Fit (20%)", f"{edu_score}%")

    st.markdown("---")

    # Display Actionable Skill Gap Blueprint
    st.subheader("🎯 Actionable Skill Gap Blueprint & Upskilling Roadmap")

    if missing_skills:
      st.warning(f"Identified Skill Deficiencies: {', '.join(missing_skills)}")
      for skill in missing_skills:
        details = skills_db.get(skill.lower(), None)
        with st.expander(f"📚 Roadmap for: {skill.upper()}"):
          if details:
            st.write(f"**Recommended Course:** [{details['course_name']}]({details['course_link']})")
            st.write(f"**Estimated Hours:** {details['estimated_hours']} Hours")
            st.write(f"**Starter Project Idea:** {details['project_idea']}")
          else:
            st.write("Free interactive tutorials available on Coursera / YouTube.")
    else:
      st.success("No critical skill gaps identified! The candidate meets all required technical skills.")