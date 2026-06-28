"""
InsideInterview AI — Main Application
"""

import os
from pathlib import Path
import streamlit as st
from config import JOB_ROLES, COLORS

st.set_page_config(
    page_title="InsideInterview AI",
    page_icon="II",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load CSS — use pathlib for reliable path resolution on Streamlit Cloud
_APP_DIR = Path(__file__).resolve().parent
css_path = _APP_DIR / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Initialize Session State
defaults = {
    "current_page": "Home",
    "job_role": "",
    "level": "",
    "assessment_score": 0,
    "section_scores": {},
    "assessment_data": None,
    "user_answers": {},
    "resume_text": "",
    "resume_analysis": None,
    "mock_state": "not_started",
    "mock_completed": False,
    "mock_summary": None,
    "mock_conversation": [],
    "mock_evaluations": [],
    "coach_history": [],
    "session_logs": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def render_home():
    """Professional home page."""

    # Hero
    st.markdown(
        f"""
        <div style="text-align: center; padding: 3rem 1rem 2rem 1rem;">
            <h1 style="
                color: {COLORS['text']};
                font-size: 2.75rem;
                font-weight: 800;
                margin: 0;
                letter-spacing: -1px;
                line-height: 1.1;
            ">Inside<span style="color: {COLORS['primary_light']};">Interview</span></h1>
            <p style="
                color: {COLORS['text_secondary']};
                font-size: 1.05rem;
                max-width: 540px;
                margin: 1rem auto 0 auto;
                line-height: 1.7;
            ">
                AI-powered interview preparation platform. Assess your skills,
                analyze your resume, and practice with realistic mock interviews.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature Cards
    features = [
        ("Smart Assessment", "20 MCQs across aptitude, verbal, and technical domains to evaluate your current level."),
        ("Resume Analysis", "Upload your resume for AI-powered scoring, gap analysis, and a personalized learning roadmap."),
        ("Mock Interviews", "Realistic interview simulations with question-by-question feedback and performance scoring."),
        ("AI Coach", "Context-aware coaching that adapts to your profile, weaknesses, and target role."),
    ]

    cols = st.columns(4)
    for col, (title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: {COLORS['bg_card']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 10px;
                    padding: 1.5rem 1.25rem;
                    height: 190px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <h3 style="color: {COLORS['text']}; font-size: 0.95rem; font-weight: 700; margin: 0 0 0.6rem 0;">
                        {title}
                    </h3>
                    <p style="color: {COLORS['text_muted']}; font-size: 0.8rem; margin: 0; line-height: 1.55;">
                        {desc}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Job Role Selection
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 0.75rem;">
            <h2 style="color: {COLORS['text']}; font-size: 1.35rem; font-weight: 700;">
                Get Started
            </h2>
            <p style="color: {COLORS['text_muted']}; font-size: 0.9rem;">
                Select your target job role to begin
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    spacer_left, center_col, spacer_right = st.columns([1, 2, 1])

    with center_col:
        selected_role = st.selectbox(
            "Target Job Role",
            options=["-- Select a role --"] + JOB_ROLES,
            index=(
                JOB_ROLES.index(st.session_state["job_role"]) + 1
                if st.session_state.get("job_role") in JOB_ROLES
                else 0
            ),
            key="role_selector",
        )

        if selected_role != "-- Select a role --":
            st.session_state["job_role"] = selected_role

            st.markdown(
                f"""
                <div style="
                    background: rgba(79, 70, 229, 0.08);
                    border: 1px solid rgba(79, 70, 229, 0.25);
                    border-radius: 8px;
                    padding: 0.85rem 1.25rem;
                    margin: 0.75rem 0;
                    text-align: center;
                ">
                    <p style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Selected Role</p>
                    <p style="color: {COLORS['primary_light']}; font-size: 1.15rem; font-weight: 700; margin: 0.2rem 0 0 0;">
                        {selected_role}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Start Assessment", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "Assessment"
                st.rerun()

    # How It Works
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align: center; margin-bottom: 1rem;'>"
        f"<h2 style='color: {COLORS['text']}; font-size: 1.15rem; font-weight: 700;'>How It Works</h2>"
        f"</div>",
        unsafe_allow_html=True,
    )

    step_cols = st.columns(5)
    steps = [
        ("01", "Select Role", "Choose your target position"),
        ("02", "Assessment", "20-question skill evaluation"),
        ("03", "Resume Analysis", "AI scoring and gap analysis"),
        ("04", "Mock Interview", "Practice with AI interviewer"),
        ("05", "Results", "Scores, feedback, and roadmap"),
    ]

    for col, (num, title, desc) in zip(step_cols, steps):
        with col:
            st.markdown(
                f"""
                <div style="text-align: center; padding: 0.5rem;">
                    <p style="
                        color: {COLORS['primary_light']};
                        font-size: 1.5rem;
                        font-weight: 800;
                        margin: 0;
                        opacity: 0.6;
                    ">{num}</p>
                    <p style="color: {COLORS['text']}; font-weight: 600; font-size: 0.85rem; margin: 0.2rem 0;">
                        {title}
                    </p>
                    <p style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin: 0;">
                        {desc}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Footer
    st.markdown(
        f"""
        <div style="text-align: center; padding: 2rem 0 0.5rem 0; margin-top: 2rem; border-top: 1px solid {COLORS['border']};">
            <p style="color: {COLORS['text_muted']}; font-size: 0.7rem;">
                InsideInterview AI &middot; Powered by Google Gemini &middot; Built with Streamlit
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Sidebar
from components.sidebar import render_sidebar
render_sidebar()

# Page Router
page = st.session_state.get("current_page", "Home")

if page == "Home":
    render_home()
elif page == "Assessment":
    from components.assessment import render_assessment
    render_assessment()
elif page == "Resume Analysis":
    from components.resume_analysis import render_resume_analysis
    render_resume_analysis()
elif page == "Mock Interview":
    from components.mock_interview import render_mock_interview
    render_mock_interview()
elif page == "AI Coach":
    from components.chat_coach import render_chat_coach
    render_chat_coach()
elif page == "Dashboard":
    from components.dashboard import render_dashboard
    render_dashboard()
elif page == "Session Logs":
    from components.session_logs import render_session_logs
    render_session_logs()
