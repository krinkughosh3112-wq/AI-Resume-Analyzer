import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Skills list (you can expand later)
SKILLS = [
    "python", "sql", "machine learning", "deep learning",
    "nlp", "data analysis", "excel", "power bi",
    "tableau", "statistics", "computer vision",
    "tensorflow", "pytorch"
]

# 🔍 Extract skills from resume
def extract_skills(text):
    text = text.lower()
    doc = nlp(text)

    found_skills = []

    for token in doc:
        if token.text in SKILLS:
            found_skills.append(token.text)

    return list(set(found_skills))


# 📄 Extract basic info (name, email)
def extract_basic_info(text):
    lines = text.split("\n")

    name = lines[0] if lines else "Not Found"

    email = re.findall(r'\S+@\S+', text)
    email = email[0] if email else "Not found"

    return {
        "Name": name.strip(),
        "Email": email
    }


# 📊 Extract expected skills from job description
def extract_expected_skills(job_desc):
    job_desc = job_desc.lower()

    expected = [skill for skill in SKILLS if skill in job_desc]

    return list(set(expected))