import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

# Load env
load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Correct model format
model = genai.GenerativeModel("models/gemini-2.5-flash")

def get_feedback(resume_text, job_desc):
    """
    Get comprehensive feedback from Gemini AI
    """
    prompt = f"""
You are an expert AI Resume Analyzer and ATS (Applicant Tracking System) specialist.

Analyze the resume against the job description in detail. Provide structured feedback.

Resume:
{resume_text[:3000]}  # Limit to avoid token limits

Job Description:
{job_desc[:2000]}  # Limit to avoid token limits

Please provide a detailed analysis in the following EXACT format:

=== ATS SCORE ===
[Calculate an ATS compatibility score out of 100 based on keyword matching, formatting, and content relevance]

=== MISSING SKILLS ===
[List all critical skills from job description that are missing in the resume]
- Skill 1
- Skill 2

=== PRESENT SKILLS ===
[List key skills from job description that are present in the resume]
- Skill 1
- Skill 2

=== KEYWORD OPTIMIZATION ===
[List important keywords from job description that should be added to improve ATS score]
- Keyword 1
- Keyword 2

=== STRENGTHS ===
[List 3-5 major strengths of this resume for this specific role]
- Strength 1
- Strength 2

=== WEAKNESSES ===
[List 3-5 areas for improvement]
- Weakness 1
- Weakness 2

=== ACTIONABLE SUGGESTIONS ===
[Provide 3-5 specific, actionable suggestions to improve the resume]
- Suggestion 1
- Suggestion 2

=== SECTION-WISE FEEDBACK ===
[Brief feedback on each resume section: Summary, Experience, Education, Skills, Projects]
- Summary: [feedback]
- Experience: [feedback]
- Education: [feedback]
- Skills: [feedback]
- Projects: [feedback]

=== OVERALL RECOMMENDATION ===
[Overall assessment: Strong Match / Good Match / Needs Improvement / Not Suitable]

Be specific, constructive, and provide actionable insights.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating feedback: {str(e)}"

def parse_feedback(feedback_text):
    """
    Parse the feedback text into structured sections
    """
    sections = {
        'ats_score': 'N/A',
        'missing_skills': [],
        'present_skills': [],
        'keywords': [],
        'strengths': [],
        'weaknesses': [],
        'suggestions': [],
        'section_feedback': {},
        'recommendation': 'N/A'
    }
    
    try:
        # Extract ATS Score
        ats_match = re.search(r'=== ATS SCORE ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if ats_match:
            ats_text = ats_match.group(1).strip()
            # Extract number from text
            score_numbers = re.findall(r'\d+', ats_text)
            if score_numbers:
                sections['ats_score'] = score_numbers[0]
            else:
                sections['ats_score'] = ats_text
        
        # Extract Missing Skills
        missing_match = re.search(r'=== MISSING SKILLS ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if missing_match:
            skills_text = missing_match.group(1).strip()
            sections['missing_skills'] = [s.strip('- ').strip() for s in skills_text.split('\n') if s.strip() and not s.startswith('===')]
        
        # Extract Present Skills
        present_match = re.search(r'=== PRESENT SKILLS ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if present_match:
            skills_text = present_match.group(1).strip()
            sections['present_skills'] = [s.strip('- ').strip() for s in skills_text.split('\n') if s.strip() and not s.startswith('===')]
        
        # Extract Keywords
        keywords_match = re.search(r'=== KEYWORD OPTIMIZATION ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if keywords_match:
            keywords_text = keywords_match.group(1).strip()
            sections['keywords'] = [k.strip('- ').strip() for k in keywords_text.split('\n') if k.strip() and not k.startswith('===')]
        
        # Extract Strengths
        strengths_match = re.search(r'=== STRENGTHS ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if strengths_match:
            strengths_text = strengths_match.group(1).strip()
            sections['strengths'] = [s.strip('- ').strip() for s in strengths_text.split('\n') if s.strip() and not s.startswith('===')]
        
        # Extract Weaknesses
        weaknesses_match = re.search(r'=== WEAKNESSES ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if weaknesses_match:
            weaknesses_text = weaknesses_match.group(1).strip()
            sections['weaknesses'] = [w.strip('- ').strip() for w in weaknesses_text.split('\n') if w.strip() and not w.startswith('===')]
        
        # Extract Suggestions
        suggestions_match = re.search(r'=== ACTIONABLE SUGGESTIONS ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if suggestions_match:
            suggestions_text = suggestions_match.group(1).strip()
            sections['suggestions'] = [s.strip('- ').strip() for s in suggestions_text.split('\n') if s.strip() and not s.startswith('===')]
        
        # Extract Section Feedback
        section_match = re.search(r'=== SECTION-WISE FEEDBACK ===\n(.*?)\n===', feedback_text, re.DOTALL)
        if section_match:
            section_text = section_match.group(1).strip()
            for line in section_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    sections['section_feedback'][key.strip('- ').strip()] = value.strip()
        
        # Extract Recommendation
        rec_match = re.search(r'=== OVERALL RECOMMENDATION ===\n(.*?)(?:\n===|$)', feedback_text, re.DOTALL)
        if rec_match:
            sections['recommendation'] = rec_match.group(1).strip()
    
    except Exception as e:
        print(f"Error parsing feedback: {e}")
    
    return sections