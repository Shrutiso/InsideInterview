"""
InsideInterview AI — Configuration & Constants
"""

import os
import streamlit as st

# ─── API Key ─────────────────────────────────────────────────
# Priority: st.secrets (Streamlit Cloud) > env var > fallback
def get_config_api_key():
    """Get API key from Streamlit secrets, environment, or fallback."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError, AttributeError):
        pass
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        return env_key
    return "AQ.Ab8RN6J9uRzZzRuKXBTq7asiHRXpS4NTkJRuPM-DtGEyIf4TXg"

GEMINI_API_KEY = get_config_api_key()

# ─── Job Roles ───────────────────────────────────────────────
JOB_ROLES = [
    "Software Engineer",
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "DevOps Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Cloud Engineer",
    "Cybersecurity Analyst",
    "Mobile App Developer",
    "AI/ML Research Scientist",
    "Database Administrator",
    "QA / Test Engineer",
    "Product Manager",
    "Business Analyst",
    "UI/UX Designer",
    "Embedded Systems Engineer",
    "Blockchain Developer",
    "Data Engineer",
]

# ─── Level thresholds (out of 20 questions) ──────────────────
LEVEL_THRESHOLDS = {
    "Advanced": 16,       # 80%+
    "Intermediate": 10,   # 50-79%
    "Beginner": 0,        # <50%
}

# ─── Color palette ───────────────────────────────────────────
COLORS = {
    "primary": "#4F46E5",
    "primary_light": "#818CF8",
    "secondary": "#E11D48",
    "accent": "#0EA5E9",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "bg_dark": "#0F172A",
    "bg_card": "#1E293B",
    "bg_card_hover": "#334155",
    "border": "#334155",
    "text": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
}

# ─── Prompt Templates ────────────────────────────────────────

ASSESSMENT_PROMPT = """You are an expert technical recruiter creating an assessment for the role of **{job_role}**.

Generate exactly 20 multiple-choice questions in the following pattern:

**Section A: Aptitude (5 questions)**
- Topics: Logical Reasoning, Quantitative Aptitude, Data Interpretation, Number Series, Probability
- Difficulty: Easy to Medium

**Section B: Verbal Ability (5 questions)**
- Topics: Reading Comprehension, Grammar, Sentence Completion, Synonyms/Antonyms, Para Jumbles
- Difficulty: Easy to Medium

**Section C: Technical (10 questions)**
- Topics: Entirely based on the role of {job_role}
- Difficulty: Easy to Hard (progressive)

For EACH question, return this exact JSON structure:

{{
  "sections": [
    {{
      "name": "Aptitude",
      "questions": [
        {{
          "id": 1,
          "question": "...",
          "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
          "correct_answer": "A",
          "difficulty": "Easy",
          "topic": "Logical Reasoning"
        }}
      ]
    }},
    {{
      "name": "Verbal Ability",
      "questions": [
        {{
          "id": 6,
          "question": "...",
          "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
          "correct_answer": "B",
          "difficulty": "Medium",
          "topic": "Grammar"
        }}
      ]
    }},
    {{
      "name": "Technical",
      "questions": [
        {{
          "id": 11,
          "question": "...",
          "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
          "correct_answer": "C",
          "difficulty": "Easy",
          "topic": "..."
        }}
      ]
    }}
  ]
}}

Return ONLY valid JSON. No extra text or markdown.
"""

RESUME_ANALYSIS_PROMPT = """You are an expert technical recruiter and career coach.

**Target Role:** {job_role}

**Candidate Level (from assessment):** {level}

**Resume Text:**
\"\"\"
{resume_text}
\"\"\"

Analyze this resume thoroughly and return a JSON response with this exact structure:

{{
  "skills": ["skill1", "skill2", "..."],
  "projects": [
    {{
      "name": "Project Name",
      "description": "Brief description",
      "technologies": ["tech1", "tech2"]
    }}
  ],
  "experience": [
    {{
      "role": "Job Title",
      "company": "Company Name",
      "duration": "Duration",
      "highlights": ["highlight1", "highlight2"]
    }}
  ],
  "education": [
    {{
      "degree": "Degree Name",
      "institution": "Institution Name",
      "year": "Year"
    }}
  ],
  "resume_score": 75,
  "strengths": ["strength1", "strength2", "..."],
  "weaknesses": ["weakness1", "weakness2", "..."],
  "missing_skills": ["skill1", "skill2", "..."],
  "improvements": ["suggestion1", "suggestion2", "..."],
  "roadmap": [
    {{
      "week": "Week 1-2",
      "focus": "Topic Area",
      "tasks": ["task1", "task2"],
      "resources": ["resource1", "resource2"]
    }}
  ],
  "interview_questions": [
    {{
      "question": "...",
      "category": "Technical/Behavioral/Situational",
      "difficulty": "Easy/Medium/Hard"
    }}
  ]
}}

Generate exactly 20 interview questions based on the resume content.
Return ONLY valid JSON. No extra text or markdown.
"""

MOCK_INTERVIEW_START_PROMPT = """You are a senior interviewer conducting a mock interview for the role of **{job_role}**.

**Candidate Profile:**
- Assessment Level: {level}
- Assessment Score: {score}/20
- Skills from Resume: {skills}
- Weak Areas: {weak_areas}

**Rules:**
1. Ask ONE question at a time.
2. Start with a brief, friendly introduction.
3. Ask your first interview question.
4. The question difficulty should match the candidate's level ({level}).
5. Focus on their weak areas: {weak_areas}

Return your response as JSON:
{{
  "interviewer_message": "Your greeting and first question...",
  "question_number": 1,
  "question_category": "Technical/Behavioral/Situational",
  "difficulty": "Easy/Medium/Hard",
  "expected_key_points": ["point1", "point2", "point3"]
}}

Return ONLY valid JSON.
"""

MOCK_INTERVIEW_EVALUATE_PROMPT = """You are a senior interviewer for the role of **{job_role}**.

**Question #{question_number}:** {question}
**Expected Key Points:** {expected_points}
**Candidate's Answer:** {answer}
**Candidate Level:** {level}

Evaluate the answer and ask the next question. Return JSON:
{{
  "evaluation": {{
    "technical_score": 8,
    "communication_score": 7,
    "confidence_score": 7,
    "feedback": "Detailed constructive feedback...",
    "key_points_covered": ["point1", "point2"],
    "missed_points": ["point3"]
  }},
  "next_question": {{
    "interviewer_message": "Feedback on previous answer + next question...",
    "question_number": {next_number},
    "question_category": "Technical/Behavioral/Situational",
    "difficulty": "Medium",
    "expected_key_points": ["point1", "point2", "point3"]
  }}
}}

Adjust difficulty based on performance. If technical_score < 5, ask an easier question. If > 8, ask harder.
Return ONLY valid JSON.
"""

MOCK_INTERVIEW_SUMMARY_PROMPT = """You are a senior interviewer. The mock interview for **{job_role}** is complete.

**All Evaluations:**
{evaluations}

Generate a comprehensive interview summary as JSON:
{{
  "overall_technical_score": 7.5,
  "overall_communication_score": 7.0,
  "overall_confidence_score": 7.0,
  "overall_rating": "Good",
  "strengths": ["strength1", "strength2"],
  "weak_areas": ["area1", "area2"],
  "recommended_topics": ["topic1", "topic2", "topic3"],
  "detailed_feedback": "Comprehensive paragraph of feedback...",
  "suggested_questions_to_practice": [
    "question1",
    "question2",
    "question3",
    "question4",
    "question5"
  ]
}}

Return ONLY valid JSON.
"""

COACH_SYSTEM_PROMPT = """You are InsideInterview AI Coach — a friendly, expert interview preparation assistant.

**Candidate Context:**
- Target Role: {job_role}
- Level: {level}
- Assessment Score: {score}/20
- Skills: {skills}
- Weak Areas: {weak_areas}

You have full context about this candidate. Always provide personalized, actionable advice.
When the candidate asks a question:
1. Give a clear, structured answer.
2. Relate it to their target role and skill level.
3. Provide examples when helpful.
4. Suggest follow-up topics if relevant.

Be encouraging but honest. Never give generic responses when you have personalized data.
"""
