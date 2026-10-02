# 📄 AI Resume Analyzer & Job Matcher

> **Smart Resume Screening & Explainable Career Guidance Assistant**  
> *Silver Oak University — Department of Computer Engineering*

An end-to-end NLP-powered recruitment assistant built with Streamlit, spaCy, and scikit-learn. The platform evaluates applicant resumes against target job descriptions using a transparent, multi-factor scoring engine and provides job seekers with an **Actionable Skill Gap Blueprint** to close qualification gaps.

---

## 📌 Project Overview & Key Features

* **Automated PDF Resume Parsing**: Extracts key text, technical skills, education history, and experience duration using `pdfplumber` and Regular Expressions.
* **Explainable Multi-Factor Scoring**: Replaces "black-box" applicant tracking systems (ATS) by decomposing candidate fit into three distinct sub-scores:
  * 🎯 **Hard Skills Match (50% Weight)**: Measures technical skill overlap using TF-IDF vectorization and Cosine Similarity.
  * 💼 **Experience Fit (30% Weight)**: Evaluates career duration and seniority alignment.
  * 🎓 **Education Alignment (20% Weight)**: Checks academic degree prerequisites and qualification hierarchy.
* **Actionable Skill Gap Blueprint**: Maps missing candidate skills to curated free courses, estimated study hours, and practical starter project ideas.
* **Dual-User Experience**: Built for both job seekers (for actionable feedback & roadmaps) and recruiters/HR (for objective candidate screening).

---

## 🛠️ Tech Stack & Dependencies

* **Language**: Python 3.11+
* **Frontend**: Streamlit
* **NLP & Text Parsing**: `pdfplumber`, `spaCy`, `re` (Regex)
* **Machine Learning**: `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`)
* **Knowledge Base**: JSON database (`skills_db.json`) mapping 100+ technical skills to course roadmaps
* **Version Control**: Git & GitHub

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your web browser.

## 📂 Project Directory Structure

```text
AI-Resume-Analyzer/
│── venv/                  # Isolated virtual environment (ignored by Git)
│── .gitignore             # Git ignore rule file
│── app.py                 # Main Streamlit web application script
│── skills_db.json         # Skill-to-course & project mapping knowledge base
│── requirements.txt       # Project dependencies list
└── README.md              # Project documentation
```

## 📊 Multi-Factor Evaluation Formula

$$
\text{Overall Fit Score} = (0.50 \times S_{\text{skills}}) + (0.30 \times S_{\text{exp}}) + (0.20 \times S_{\text{edu}})

| **Evaluation Metric**   | **Component Weight** | **Analysis Technique**                                           |
| ----------------------- | -------------------- | ---------------------------------------------------------------- |
| **Hard Skills Match**   | **50%**              | TF-IDF Vectorization & Cosine Similarity on extracted skill sets |
| **Experience Fit**      | **30%**              | Quantitative regex parsing against target role requirements      |
| **Education Alignment** | **20%**              | Degree hierarchy validation (B.Tech, M.Tech, MCA, etc.)          |
$$