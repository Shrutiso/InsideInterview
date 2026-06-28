"""
InsideInterview AI — Resume Analysis Component
"""

import streamlit as st
from config import COLORS
from utils.gemini_client import analyze_resume
from utils.resume_parser import parse_resume
from utils.helpers import get_score_color


def render_resume_analysis():
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1 style="color: {COLORS['text']}; font-size: 2rem; font-weight: 800;">Resume Analysis</h1>
            <p style="color: {COLORS['text_muted']}; font-size: 0.95rem;">
                Upload your resume for AI-powered analysis and gap identification
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.get("level"):
        st.warning("Please complete the assessment first.")
        return

    if st.session_state.get("resume_analysis"):
        _render_analysis_results()
        return

    # Upload
    st.markdown(
        f"""
        <div style="
            background: {COLORS['bg_card']};
            border: 2px dashed {COLORS['border']};
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
        ">
            <p style="color: {COLORS['text']}; font-weight: 600; font-size: 1.05rem; margin: 0 0 0.3rem 0;">
                Upload Your Resume
            </p>
            <p style="color: {COLORS['text_muted']}; font-size: 0.8rem; margin: 0;">
                Supported formats: PDF, DOCX
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx"], key="resume_uploader", label_visibility="collapsed")

    if uploaded_file:
        with st.spinner("Extracting text from resume..."):
            resume_text = parse_resume(uploaded_file)

        if resume_text.startswith("Error") or resume_text.startswith("Unsupported"):
            st.error(resume_text)
            return

        st.session_state["resume_text"] = resume_text

        with st.expander("Extracted Resume Text", expanded=False):
            st.text(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))

        if st.button("Analyze Resume with AI", use_container_width=True, type="primary"):
            with st.spinner("AI is analyzing your resume... This may take a moment."):
                try:
                    analysis = analyze_resume(
                        job_role=st.session_state.get("job_role", ""),
                        level=st.session_state.get("level", ""),
                        resume_text=resume_text,
                    )
                except Exception as e:
                    analysis = None
                    st.error(f"Error during analysis: {str(e)}")

            if analysis:
                st.session_state["resume_analysis"] = analysis
                if "session_logs" not in st.session_state:
                    st.session_state["session_logs"] = []
                st.session_state["session_logs"].append({
                    "event": "Resume Analyzed",
                    "score": analysis.get("resume_score", "N/A"),
                })
                st.rerun()
            else:
                st.error("Failed to analyze resume. Please try again.")


def _render_analysis_results():
    analysis = st.session_state["resume_analysis"]
    job_role = st.session_state.get("job_role", "")

    score = analysis.get("resume_score", 0)
    score_color = get_score_color(score, 100)

    # Score Card
    st.markdown(
        f"""
        <div style="
            background: {COLORS['bg_card']};
            border: 1px solid {score_color}35;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <p style="color: {COLORS['text_muted']}; font-size: 0.8rem; margin: 0;">
                Resume Score for <b style="color: {COLORS['text']};">{job_role}</b>
            </p>
            <p style="color: {score_color}; font-size: 3rem; font-weight: 800; margin: 0.5rem 0;">
                {score}<span style="font-size: 1.1rem; color: {COLORS['text_muted']};">/100</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Skills & Education
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='color: {COLORS['text']}; font-size: 1rem; margin-bottom: 0.75rem;'>Extracted Skills</h3>", unsafe_allow_html=True)
        skills = analysis.get("skills", [])
        if skills:
            tags = " ".join(
                f'<span style="background:{COLORS["primary"]}18; color:{COLORS["primary_light"]}; '
                f'padding:4px 12px; border-radius:4px; font-size:0.78rem; display:inline-block; '
                f'margin:2px; border: 1px solid {COLORS["primary"]}30;">{s}</span>' for s in skills
            )
            st.markdown(tags, unsafe_allow_html=True)

    with col2:
        st.markdown(f"<h3 style='color: {COLORS['text']}; font-size: 1rem; margin-bottom: 0.75rem;'>Education</h3>", unsafe_allow_html=True)
        for edu in analysis.get("education", []):
            st.markdown(f"**{edu.get('degree', 'N/A')}** -- {edu.get('institution', 'N/A')} ({edu.get('year', 'N/A')})")

    # Projects
    projects = analysis.get("projects", [])
    if projects:
        st.markdown(f"<br><h3 style='color: {COLORS['text']}; font-size: 1rem;'>Projects</h3>", unsafe_allow_html=True)
        for proj in projects:
            techs = ", ".join(proj.get("technologies", []))
            st.markdown(
                f"""
                <div style="background:{COLORS['bg_card']}; border-left:3px solid {COLORS['accent']};
                    border-radius:0 6px 6px 0; padding:0.7rem 1rem; margin:0.4rem 0;">
                    <p style="color:{COLORS['text']}; font-weight:600; margin:0; font-size:0.88rem;">{proj.get('name', '')}</p>
                    <p style="color:{COLORS['text_muted']}; font-size:0.78rem; margin:0.15rem 0 0 0;">{proj.get('description', '')}</p>
                    <p style="color:{COLORS['primary_light']}; font-size:0.72rem; margin:0.15rem 0 0 0;">{techs}</p>
                </div>
                """, unsafe_allow_html=True)

    # Experience
    experience = analysis.get("experience", [])
    if experience:
        st.markdown(f"<br><h3 style='color: {COLORS['text']}; font-size: 1rem;'>Experience</h3>", unsafe_allow_html=True)
        for exp in experience:
            highlights = "".join(f"<li>{h}</li>" for h in exp.get("highlights", []))
            st.markdown(
                f"""
                <div style="background:{COLORS['bg_card']}; border-left:3px solid {COLORS['success']};
                    border-radius:0 6px 6px 0; padding:0.7rem 1rem; margin:0.4rem 0;">
                    <p style="color:{COLORS['text']}; font-weight:600; margin:0;">{exp.get('role', '')} at {exp.get('company', '')}</p>
                    <p style="color:{COLORS['text_muted']}; font-size:0.78rem; margin:0.15rem 0;">{exp.get('duration', '')}</p>
                    <ul style="color:{COLORS['text_muted']}; font-size:0.78rem; margin:0; padding-left:1.25rem;">{highlights}</ul>
                </div>
                """, unsafe_allow_html=True)

    # Gap Analysis
    st.markdown(f"<br><h3 style='color: {COLORS['text']}; font-size: 1.1rem;'>Gap Analysis</h3>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)

    with g1:
        st.markdown(f"<h4 style='color: {COLORS['success']}; font-size: 0.9rem;'>Strengths</h4>", unsafe_allow_html=True)
        for s in analysis.get("strengths", []): st.markdown(f"- {s}")
        st.markdown(f"<h4 style='color: {COLORS['danger']}; font-size: 0.9rem;'>Weaknesses</h4>", unsafe_allow_html=True)
        for w in analysis.get("weaknesses", []): st.markdown(f"- {w}")

    with g2:
        st.markdown(f"<h4 style='color: {COLORS['warning']}; font-size: 0.9rem;'>Missing Skills</h4>", unsafe_allow_html=True)
        missing = analysis.get("missing_skills", [])
        if missing:
            tags = " ".join(
                f'<span style="background:{COLORS["danger"]}15; color:{COLORS["danger"]}; '
                f'padding:4px 10px; border-radius:4px; font-size:0.78rem; display:inline-block; margin:2px;">{s}</span>' for s in missing
            )
            st.markdown(tags, unsafe_allow_html=True)
        st.markdown(f"<h4 style='color: {COLORS['accent']}; font-size: 0.9rem;'>Suggested Improvements</h4>", unsafe_allow_html=True)
        for imp in analysis.get("improvements", []): st.markdown(f"- {imp}")

    # Roadmap
    roadmap = analysis.get("roadmap", [])
    if roadmap:
        st.markdown(f"<br><h3 style='color: {COLORS['text']}; font-size: 1.1rem;'>Personalized Learning Roadmap</h3>", unsafe_allow_html=True)
        for phase in roadmap:
            tasks = "".join(f"<li>{t}</li>" for t in phase.get("tasks", []))
            resources = "".join(f"<li>{r}</li>" for r in phase.get("resources", []))
            st.markdown(
                f"""
                <div style="background:{COLORS['bg_card']}; border:1px solid {COLORS['border']};
                    border-radius:8px; padding:1rem 1.25rem; margin:0.6rem 0;">
                    <h4 style="color:{COLORS['primary_light']}; margin:0; font-size:0.9rem;">
                        {phase.get('week', '')} -- {phase.get('focus', '')}</h4>
                    <div style="display:flex; gap:2rem; margin-top:0.4rem;">
                        <div><p style="color:{COLORS['text']}; font-size:0.78rem; font-weight:600; margin:0;">Tasks:</p>
                            <ul style="color:{COLORS['text_muted']}; font-size:0.78rem; padding-left:1.25rem; margin:0.2rem 0 0 0;">{tasks}</ul></div>
                        <div><p style="color:{COLORS['text']}; font-size:0.78rem; font-weight:600; margin:0;">Resources:</p>
                            <ul style="color:{COLORS['text_muted']}; font-size:0.78rem; padding-left:1.25rem; margin:0.2rem 0 0 0;">{resources}</ul></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Interview Questions
    interview_qs = analysis.get("interview_questions", [])
    if interview_qs:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("20 Interview Questions Based on Your Resume"):
            for i, q in enumerate(interview_qs, 1):
                diff = q.get("difficulty", "Medium")
                diff_color = {"Easy": COLORS["success"], "Medium": COLORS["warning"], "Hard": COLORS["danger"]}.get(diff, COLORS["warning"])
                st.markdown(
                    f"""<div style="background:{COLORS['bg_card']}; border-radius:6px; padding:0.5rem 1rem; margin:0.3rem 0;
                        display:flex; align-items:center; gap:0.5rem;">
                        <span style="color:{COLORS['primary_light']}; font-weight:700; font-size:0.8rem; min-width:24px;">{i}.</span>
                        <span style="color:{COLORS['text']}; font-size:0.83rem; flex:1;">{q.get('question', '')}</span>
                        <span style="background:{diff_color}15; color:{diff_color}; font-size:0.6rem; padding:2px 8px;
                            border-radius:4px; font-weight:600; text-transform:uppercase;">{diff}</span>
                    </div>""", unsafe_allow_html=True)

    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start Mock Interview", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "Mock Interview"
            st.rerun()
    with c2:
        if st.button("View Dashboard", use_container_width=True):
            st.session_state["current_page"] = "Dashboard"
            st.rerun()
