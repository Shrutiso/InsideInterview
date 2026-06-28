"""
InsideInterview AI — Assessment Component
"""

import streamlit as st
from config import COLORS
from utils.gemini_client import generate_assessment
from utils.helpers import (
    classify_level,
    calculate_section_scores,
    calculate_total_score,
)


def render_assessment():
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1 style="color: {COLORS['text']}; font-size: 2rem; font-weight: 800;">
                Initial Assessment
            </h1>
            <p style="color: {COLORS['text_muted']}; font-size: 0.95rem;">
                Complete this assessment to evaluate your current skill level
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_role = st.session_state.get("job_role", "")
    if not job_role:
        st.warning("Please select a job role from the Home page first.")
        return

    if st.session_state.get("level"):
        _render_results()
        return

    # Generate assessment
    if not st.session_state.get("assessment_data"):
        with st.spinner("Generating personalized assessment for **{}**...".format(job_role)):
            try:
                data = generate_assessment(job_role)
            except Exception as e:
                data = None
                st.error(f"Error generating assessment: {str(e)}")

        if data and "sections" in data:
            st.session_state["assessment_data"] = data
            st.rerun()
        else:
            st.error("Failed to generate assessment. Please try again.")
            if st.button("Retry"):
                st.rerun()
            return

    assessment_data = st.session_state["assessment_data"]

    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = {}

    with st.form("assessment_form"):
        for section in assessment_data["sections"]:
            section_name = section["name"]
            question_count = len(section["questions"])

            st.markdown(
                f"""
                <div style="
                    background: {COLORS['bg_card']};
                    border-left: 3px solid {COLORS['primary']};
                    border-radius: 0 8px 8px 0;
                    padding: 0.85rem 1.25rem;
                    margin: 1.5rem 0 1rem 0;
                ">
                    <h2 style="color: {COLORS['text']}; margin: 0; font-size: 1.15rem;">
                        Section: {section_name}
                    </h2>
                    <p style="color: {COLORS['text_muted']}; margin: 0.2rem 0 0 0; font-size: 0.8rem;">
                        {question_count} Questions
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for q in section["questions"]:
                q_id = str(q["id"])
                difficulty = q.get("difficulty", "Medium")
                topic = q.get("topic", "General")
                diff_color = {
                    "Easy": COLORS["success"], "Medium": COLORS["warning"], "Hard": COLORS["danger"],
                }.get(difficulty, COLORS["warning"])

                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; gap:0.6rem; margin-top:1.1rem; margin-bottom:0.2rem;">
                        <span style="background:{COLORS['primary']}20; color:{COLORS['primary_light']};
                            font-weight:700; font-size:0.7rem; padding:2px 10px; border-radius:4px;">Q{q_id}</span>
                        <span style="background:{diff_color}15; color:{diff_color};
                            font-size:0.6rem; padding:2px 8px; border-radius:4px;
                            text-transform:uppercase; font-weight:600;">{difficulty}</span>
                        <span style="color:{COLORS['text_muted']}; font-size:0.65rem;">{topic}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                options = q["options"]
                option_map = {}
                for opt in options:
                    letter = opt.strip()[0]
                    option_map[opt] = letter

                selected = st.radio(q["question"], options=options, key=f"q_{q_id}", index=None)
                if selected:
                    st.session_state["user_answers"][q_id] = option_map.get(selected, selected[0])

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Assessment", use_container_width=True, type="primary")

        if submitted:
            answers = st.session_state.get("user_answers", {})
            total_questions = sum(len(s["questions"]) for s in assessment_data["sections"])

            if len(answers) < total_questions:
                st.warning(f"You've answered {len(answers)}/{total_questions} questions. Please answer all.")
            else:
                total_score = calculate_total_score(answers, assessment_data)
                section_scores = calculate_section_scores(answers, assessment_data)
                level = classify_level(total_score)

                st.session_state["assessment_score"] = total_score
                st.session_state["section_scores"] = section_scores
                st.session_state["level"] = level

                if "session_logs" not in st.session_state:
                    st.session_state["session_logs"] = []
                st.session_state["session_logs"].append({
                    "event": "Assessment Completed",
                    "score": f"{total_score}/20",
                    "level": level,
                })
                st.rerun()


def _render_results():
    score = st.session_state.get("assessment_score", 0)
    level = st.session_state.get("level", "Unknown")
    section_scores = st.session_state.get("section_scores", {})
    assessment_data = st.session_state.get("assessment_data", {})
    answers = st.session_state.get("user_answers", {})

    level_color = {
        "Beginner": COLORS["danger"], "Intermediate": COLORS["warning"], "Advanced": COLORS["success"],
    }.get(level, COLORS["primary"])

    # Score Overview
    st.markdown(
        f"""
        <div style="
            background: {COLORS['bg_card']};
            border: 1px solid {level_color}35;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <h2 style="color: {level_color}; font-size: 1.5rem; font-weight: 800; margin: 0;">
                {level} Level
            </h2>
            <p style="color: {COLORS['text']}; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">
                {score}<span style="color: {COLORS['text_muted']}; font-size: 1.1rem;">/20</span>
            </p>
            <p style="color: {COLORS['text_muted']}; font-size: 0.85rem;">Overall Assessment Score</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section Scores
    cols = st.columns(len(section_scores))
    for col, (name, scores) in zip(cols, section_scores.items()):
        pct = scores["percentage"]
        pct_color = COLORS["success"] if pct >= 80 else (COLORS["warning"] if pct >= 50 else COLORS["danger"])
        with col:
            st.markdown(
                f"""
                <div style="
                    background: {COLORS['bg_card']};
                    border-radius: 10px;
                    padding: 1.25rem;
                    text-align: center;
                    border: 1px solid {COLORS['border']};
                ">
                    <p style="color: {COLORS['text']}; font-weight: 600; font-size: 0.85rem; margin: 0 0 0.3rem 0;">
                        {name}
                    </p>
                    <p style="color: {pct_color}; font-size: 1.5rem; font-weight: 700; margin: 0;">
                        {scores['correct']}/{scores['total']}
                    </p>
                    <p style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin: 0;">{pct}%</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Answer Key
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("View Answer Key", expanded=False):
        for section in assessment_data.get("sections", []):
            st.markdown(f"### {section['name']}")
            for q in section["questions"]:
                q_id = str(q["id"])
                user_ans = answers.get(q_id, "--")
                correct_ans = q["correct_answer"]
                is_correct = user_ans == correct_ans
                status = "CORRECT" if is_correct else "INCORRECT"
                status_color = COLORS["success"] if is_correct else COLORS["danger"]

                st.markdown(
                    f"""
                    <div style="
                        background: {COLORS['bg_card']};
                        border-left: 3px solid {status_color};
                        border-radius: 0 6px 6px 0;
                        padding: 0.6rem 1rem;
                        margin: 0.4rem 0;
                    ">
                        <p style="color: {COLORS['text']}; font-weight: 600; margin: 0; font-size: 0.85rem;">
                            Q{q_id}: {q['question']}
                        </p>
                        <p style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin: 0.2rem 0 0 0;">
                            Your Answer: <b>{user_ans}</b> &nbsp;|&nbsp;
                            Correct: <b style="color: {COLORS['success']};">{correct_ans}</b> &nbsp;|&nbsp;
                            {status}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload Resume", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "Resume Analysis"
            st.rerun()
    with col2:
        if st.button("Retake Assessment", use_container_width=True):
            for key in ["assessment_data", "user_answers", "assessment_score", "section_scores", "level"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
