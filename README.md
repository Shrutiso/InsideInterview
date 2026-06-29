# InsideInterview
# 🚀 InsideInterview – AI-Powered Personalized Interview Preparation Platform

🔗 **Live Demo:** https://insideinterview.streamlit.app/

## 🚀 Running the Project from the Live Demo

**Live Demo:** https://insideinterview.streamlit.app/

### Before You Start

Due to usage limits and security restrictions of the Google Gemini API, users need to provide their **own Gemini API Key** to use the AI-powered features of the application.

Without configuring the API key, features such as:

* AI Assessments
* Resume Analysis
* Mock Interviews
* AI Career Coach
* Personalized Roadmaps

will not function.

---

### Steps to Run the Application

#### Step 1: Open the Live Demo

Visit:

```text
https://insideinterview.streamlit.app/
```

#### Step 2: Generate Your Gemini API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account.
3. Click **Create API Key**.
4. Copy the generated API key.

#### Step 3: Configure the API Key

Inside the application, click on **Configure API Key** from the sidebar or settings section.

Paste your Gemini API key and save it.

#### Step 4: Start Using the Platform

Once the API key is configured, all features of InsideInterview will work seamlessly, including:

 Personalized Assessments

 Resume Analysis

 Mock Interviews

 AI Interview Coach

 Dashboard & Analytics

---

> **Note:** The API key is used only for making requests to Google's Gemini API and is not stored permanently by the application. Users can replace their API key at any time.


---

# 📌 Overview

InsideInterview is an AI-powered interview preparation platform that helps students and job seekers prepare for their dream roles through personalized assessments, resume analysis, AI-powered mock interviews, and performance tracking.

Unlike generic interview preparation platforms, InsideInterview adapts according to:

* 🎯 Target Job Role
* 📊 Current Skill Level
* 📄 Resume
* 📝 Assessment Performance
* 📈 Areas of Improvement

The platform acts as an **AI Career Mentor** and **Personalized Interview Coach**.

---

# 🎯 Problem Statement

Most candidates prepare for interviews using generic question banks and random resources. They often do not know:

* Their current preparation level.
* Skills required for a specific role.
* Gaps in their resume.
* Which topics to focus on.
* How they would perform in an actual interview.

InsideInterview solves these problems by providing a personalized preparation journey.

---

# ✨ Features

## 1. Target Job Role Selection

Candidates can choose roles such as:

* AI Engineer
* Software Engineer
* Data Analyst
* Data Engineer
* Backend Developer
* Frontend Developer
* Product Manager
* Custom Role

---

## 2. Initial Assessment Test

The platform conducts an assessment consisting of:

### Aptitude

* Quantitative Aptitude
* Logical Reasoning
* Data Interpretation

### Verbal Ability

* Grammar
* Vocabulary
* Reading Comprehension

### Technical Questions

Questions generated dynamically according to the selected role.

---

## 3. Skill Level Classification

Based on assessment scores, users are classified into:

* Beginner
* Intermediate
* Advanced

---

## 4. Resume Analysis

The system extracts:

* Skills
* Projects
* Experience
* Education

The AI provides:

* Resume Score
* Strengths
* Weaknesses
* Missing Skills
* Suggestions for Improvement

---

## 5. Resume Gap Analysis

Compares:

**Candidate Resume VS Target Role Requirements**

Identifies:

* Missing Technologies
* Weak Areas
* Skills to Improve
* Recommended Projects

---

## 6. Personalized Learning Roadmap

Generates:

* Topics to Learn
* Weekly Study Plan
* Personalized Learning Path

---

## 7. AI Interview Preparation Assistant

Users can ask:

* Explain HashMap.
* What is LangChain?
* Ask me SQL interview questions.
* Explain Machine Learning.

---

## 8. Mock Interview System

Features:

* One question at a time
* Dynamic difficulty adjustment
* Follow-up questions
* Resume-based questions
* Personalized feedback

---

## 9. AI Feedback System

Evaluates:

* Technical Accuracy
* Communication Skills
* Confidence
* Problem Solving Ability

Provides:

* Strengths
* Weak Areas
* Suggestions for Improvement

---

## 10. Dashboard & Analytics

Displays:

* Assessment Scores
* Progress Tracking
* Strong Topics
* Weak Topics
* Performance Trends

---

## 11. Session Logs

Stores:

* Assessment Results
* Mock Interviews
* AI Responses
* Feedback Reports

---

# 🏗️ System Architecture

```text id="v8kru6"
User
 ↓
Streamlit Frontend
 ↓
Python Backend Services
 ↓
Google Gemini API
 ↓
SQLite Database
 ↓
Dashboard & Analytics
```

---

# ⚙️ Tech Stack

| Category        | Technology       |
| --------------- | ---------------- |
| Frontend        | Streamlit        |
| Backend         | Python           |
| AI Model        | Google Gemini    |
| Framework       | LangChain        |
| Database        | SQLite           |
| Data Processing | Pandas           |
| PDF Processing  | PyPDF2 / PyMuPDF |
| Visualization   | Plotly           |

---

# 📂 Project Structure

```text id="x8dnjg"
InsideInterview/
│
├── app.py
├── components/
├── services/
├── database/
├── data/
├── logs/
├── assets/
├── requirements.txt
└── README.md
```

---

# 🚀 How to Run the Project

## 1. Clone Repository

```bash id="eoz9n4"
git clone <repository-link>
cd InsideInterview
```

## 2. Create Virtual Environment

```bash id="t9wgo3"
python -m venv venv
```

## 3. Activate Environment

Windows:

```bash id="ndb4lq"
venv\Scripts\activate
```

Linux/Mac:

```bash id="vk9t7i"
source venv/bin/activate
```

## 4. Install Dependencies

```bash id="c3j2mi"
pip install -r requirements.txt
```

## 5. Configure API Key

Create:

```text id="w5x5yu"
.streamlit/secrets.toml
```

Add:

```toml id="gqmsm8"
GEMINI_API_KEY = "YOUR_API_KEY"
```

## 6. Run Application

```bash id="pr8yg5"
streamlit run app.py
```

Application runs on:

```text id="j4fgjg"
http://localhost:8501
```

---

# ⚙️ How It Works

1. User selects a target role.
2. System generates a personalized assessment.
3. User takes the assessment.
4. AI determines the user's skill level.
5. Resume is analyzed.
6. Resume gaps are identified.
7. Personalized roadmap is generated.
8. User practices through mock interviews.
9. AI generates detailed feedback.
10. Dashboard tracks progress.

---

# 🎯 Key Decisions & Trade-Offs

## Why Streamlit?

* Rapid development
* Easy deployment
* Interactive UI

Trade-off:

* Less customizable than React.

---

## Why Google Gemini?

* Strong reasoning capabilities
* Structured JSON generation
* Cost-effective

Trade-off:

* Occasional formatting inconsistencies.

---

## Why SQLite?

* Lightweight
* Easy deployment
* No server setup

Trade-off:

* Not suitable for large-scale production.

---

## What Was Left Out?

* Authentication System
* Voice Interviews
* Multi-Agent Architecture
* Vector Database
* Cloud Infrastructure

---

# 📊 Example Runs

## Example 1

Role: AI Engineer

Assessment Score: 16/20

Level: Advanced

Resume Score: 82/100

Missing Skills:

* Docker
* MLOps
* LangGraph

---

## Example 2

Role: Backend Developer

Assessment Score: 10/20

Level: Intermediate

Resume Score: 68/100

Missing Skills:

* Redis
* System Design
* Microservices

---

## Example 3

Role: Data Analyst

Assessment Score: 8/20

Level: Beginner

Missing Skills:

* Power BI
* Statistics
* Advanced SQL

---

# 🔮 Future Improvements

* Voice-based Interviews
* Authentication System
* Vector Database Integration (FAISS)
* Multi-Agent Architecture using LangGraph
* Real-Time Interview Analytics
* AWS Deployment
* Company-Specific Interview Preparation
* Resume ATS Scoring

---

# 🧠 LLM Chat Session Logs

This project was built with extensive assistance from AI tools including Google Gemini and ChatGPT.

AI was used for:

* System Design
* Prompt Engineering
* Architecture Planning
* Resume Analysis Logic
* Mock Interview Design
* Dashboard Improvements
* Error Handling
* Deployment Support

The development process involved continuous interactions with LLMs to iteratively improve the platform and refine prompts.

---

# 👩‍💻 Developed By

**Shruti Somvanshi**

If you found this project useful, please consider giving it a ⭐ on GitHub.
