"""
InsideInterview AI — Mock Interview Component
"""

import streamlit as st
from config import COLORS
from utils.gemini_client import (
    start_mock_interview,
    evaluate_mock_answer,
    generate_interview_summary,
)

MAX_QUESTIONS = 8


def render_mock_interview():
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1 style="color: {COLORS['text']}; font-size: 2rem; font-weight: 800;">Mock Interview</h1>
            <p style="color: {COLORS['text_muted']}; font-size: 0.95rem;">
                AI-powered interview simulation with real-time feedback
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.get("resume_analysis"):
        st.warning("Please complete resume analysis first.")
        return

    if st.session_state.get("mock_summary"):
        _render_summary()
        return

    if "mock_state" not in st.session_state:
        st.session_state["mock_state"] = "not_started"

    if st.session_state["mock_state"] == "not_started":
        _render_start_screen()
    elif st.session_state["mock_state"] == "in_progress":
        _render_interview()


def _render_start_screen():
    job_role = st.session_state.get("job_role", "")
    level = st.session_state.get("level", "")
    score = st.session_state.get("assessment_score", 0)
    resume_analysis = st.session_state.get("resume_analysis", {})
    skills = resume_analysis.get("skills", [])
    weak_areas = resume_analysis.get("weaknesses", []) + resume_analysis.get("missing_skills", [])

    st.markdown(
        f"""
        <div style="background:{COLORS['bg_card']}; border:1px solid {COLORS['border']};
            border-radius:12px; padding:1.75rem; margin-bottom:1.5rem;">
            <h3 style="color:{COLORS['text']}; margin:0 0 1rem 0; font-size: 1.05rem;">Interview Details</h3>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
                <div><p style="color:{COLORS['text_muted']}; font-size:0.75rem; margin:0;">Target Role</p>
                    <p style="color:{COLORS['primary_light']}; font-weight:600; margin:0;">{job_role}</p></div>
                <div><p style="color:{COLORS['text_muted']}; font-size:0.75rem; margin:0;">Your Level</p>
                    <p style="color:{COLORS['accent']}; font-weight:600; margin:0;">{level}</p></div>
                <div><p style="color:{COLORS['text_muted']}; font-size:0.75rem; margin:0;">Assessment Score</p>
                    <p style="color:{COLORS['text']}; font-weight:600; margin:0;">{score}/20</p></div>
                <div><p style="color:{COLORS['text_muted']}; font-size:0.75rem; margin:0;">Questions</p>
                    <p style="color:{COLORS['text']}; font-weight:600; margin:0;">{MAX_QUESTIONS}</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="background:{COLORS['bg_card']}; border-radius:10px; padding:1rem 1.25rem;
            border:1px solid {COLORS['border']}; margin-bottom:1.5rem;">
            <p style="color:{COLORS['text']}; font-weight:600; margin:0 0 0.4rem 0; font-size: 0.85rem;">Tips</p>
            <ul style="color:{COLORS['text_muted']}; font-size:0.82rem; margin:0; padding-left:1.25rem;">
                <li>Answer as if you are in a real interview</li>
                <li>Be specific and use examples from your experience</li>
                <li>The AI adapts difficulty based on your answers</li>
                <li>You will receive feedback after each question</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Start Mock Interview", use_container_width=True, type="primary"):
        with st.spinner("Your interviewer is preparing..."):
            try:
                result = start_mock_interview(job_role=job_role, level=level, score=score, skills=skills, weak_areas=weak_areas[:5])
            except Exception as e:
                result = None
                st.error(f"Error preparing interview: {str(e)}")
                return

        if result:
            st.session_state["mock_state"] = "in_progress"
            st.session_state["mock_questions"] = [result]
            st.session_state["mock_evaluations"] = []
            st.session_state["mock_current_q"] = 0
            st.session_state["mock_conversation"] = [{"role": "interviewer", "content": result.get("interviewer_message", "Let's begin."), "question_number": 1}]
            if "session_logs" not in st.session_state: st.session_state["session_logs"] = []
            st.session_state["session_logs"].append({"event": "Mock Interview Started"})
            st.rerun()
        else:
            st.error("Failed to start interview. Please try again.")


def _render_interview():
    conversation = st.session_state.get("mock_conversation", [])
    current_q = st.session_state.get("mock_current_q", 0)

    progress = min(current_q + 1, MAX_QUESTIONS) / MAX_QUESTIONS
    st.progress(progress, text=f"Question {min(current_q + 1, MAX_QUESTIONS)} of {MAX_QUESTIONS}")

    for msg in conversation:
        if msg["role"] == "interviewer":
            st.markdown(
                f"""<div style="background:rgba(79,70,229,0.08); border-left:3px solid {COLORS['primary']};
                    border-radius:0 10px 10px 0; padding:0.85rem 1.25rem; margin:0.6rem 0;">
                    <p style="color:{COLORS['primary_light']}; font-weight:600; font-size:0.7rem; margin:0 0 0.3rem 0;
                        text-transform:uppercase; letter-spacing:1px;">Interviewer</p>
                    <p style="color:{COLORS['text']}; font-size:0.88rem; margin:0; line-height:1.65;">{msg['content']}</p>
                </div>""", unsafe_allow_html=True)
        elif msg["role"] == "candidate":
            st.markdown(
                f"""<div style="background:{COLORS['bg_card']}; border-right:3px solid {COLORS['accent']};
                    border-radius:10px 0 0 10px; padding:0.85rem 1.25rem; margin:0.6rem 0 0.6rem 2rem;">
                    <p style="color:{COLORS['accent']}; font-weight:600; font-size:0.7rem; margin:0 0 0.3rem 0;
                        text-transform:uppercase; letter-spacing:1px;">You</p>
                    <p style="color:{COLORS['text']}; font-size:0.88rem; margin:0; line-height:1.65;">{msg['content']}</p>
                </div>""", unsafe_allow_html=True)
        elif msg["role"] == "feedback":
            st.markdown(
                f"""<div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.2);
                    border-radius:8px; padding:0.65rem 1rem; margin:0.4rem 0 0.4rem 1rem;">
                    <p style="color:{COLORS['success']}; font-weight:600; font-size:0.65rem; margin:0 0 0.2rem 0;
                        text-transform:uppercase; letter-spacing:1px;">Feedback</p>
                    <p style="color:{COLORS['text_secondary']}; font-size:0.8rem; margin:0; line-height:1.5;">{msg['content']}</p>
                </div>""", unsafe_allow_html=True)

    if current_q < MAX_QUESTIONS:
        answer = st.text_area("Your Answer", key=f"mock_answer_{current_q}", height=120, placeholder="Type your answer here...")
        c1, c2 = st.columns([3, 1])
        with c1:
            if st.button("Submit Answer", use_container_width=True, type="primary"):
                if not answer or not answer.strip():
                    st.warning("Please provide an answer before submitting.")
                    return
                _submit_answer(answer.strip())
        with c2:
            if st.button("End Interview", use_container_width=True):
                _end_interview()
    else:
        _end_interview()


def _submit_answer(answer):
    current_q = st.session_state.get("mock_current_q", 0)
    questions = st.session_state.get("mock_questions", [])
    if not questions: return

    current_question_data = questions[-1]
    job_role = st.session_state.get("job_role", "")
    level = st.session_state.get("level", "")

    st.session_state["mock_conversation"].append({"role": "candidate", "content": answer})

    with st.spinner("Evaluating your answer..."):
        try:
            result = evaluate_mock_answer(
                job_role=job_role, level=level,
                question_number=current_question_data.get("question_number", current_q + 1),
                question=current_question_data.get("interviewer_message", ""),
                expected_points=current_question_data.get("expected_key_points", []),
                answer=answer,
            )
        except Exception as e:
            result = None
            st.error(f"Error evaluating answer: {str(e)}")
            return

    if result:
        evaluation = result.get("evaluation", {})
        next_q = result.get("next_question", {})
        st.session_state["mock_evaluations"].append(evaluation)

        feedback_text = (
            f"Technical: {evaluation.get('technical_score', 'N/A')}/10 | "
            f"Communication: {evaluation.get('communication_score', 'N/A')}/10 | "
            f"Confidence: {evaluation.get('confidence_score', 'N/A')}/10 --- "
            f"{evaluation.get('feedback', '')}"
        )
        st.session_state["mock_conversation"].append({"role": "feedback", "content": feedback_text})

        new_q = current_q + 1
        st.session_state["mock_current_q"] = new_q

        if new_q < MAX_QUESTIONS and next_q:
            st.session_state["mock_questions"].append(next_q)
            st.session_state["mock_conversation"].append({
                "role": "interviewer",
                "content": next_q.get("interviewer_message", "Next question..."),
                "question_number": next_q.get("question_number", new_q + 1),
            })
        st.rerun()
    else:
        st.error("Failed to evaluate answer. Please try again.")


def _end_interview():
    evaluations = st.session_state.get("mock_evaluations", [])
    if not evaluations:
        st.warning("No answers to evaluate.")
        return

    with st.spinner("Generating your interview report..."):
        try:
            summary = generate_interview_summary(st.session_state.get("job_role", ""), evaluations)
        except Exception as e:
            summary = None
            st.error(f"Error generating summary: {str(e)}")
            return

    if summary:
        st.session_state["mock_summary"] = summary
        st.session_state["mock_completed"] = True
        if "session_logs" not in st.session_state: st.session_state["session_logs"] = []
        st.session_state["session_logs"].append({
            "event": "Mock Interview Completed",
            "overall_rating": summary.get("overall_rating", "N/A"),
        })
        st.rerun()
    else:
        st.error("Failed to generate summary.")


def _render_summary():
    summary = st.session_state["mock_summary"]
    tech = summary.get("overall_technical_score", 0)
    comm = summary.get("overall_communication_score", 0)
    conf = summary.get("overall_confidence_score", 0)
    rating = summary.get("overall_rating", "N/A")

    rating_color = COLORS["success"] if tech >= 7 else (COLORS["warning"] if tech >= 5 else COLORS["danger"])

    st.markdown(
        f"""<div style="background:{COLORS['bg_card']}; border:1px solid {rating_color}35;
            border-radius:12px; padding:2rem; text-align:center; margin-bottom:2rem;">
            <h2 style="color:{rating_color}; font-size:1.5rem; font-weight:800; margin:0;">{rating}</h2>
            <p style="color:{COLORS['text_muted']}; font-size:0.85rem; margin:0.3rem 0 0 0;">Mock Interview Performance</p>
        </div>""",
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    scores = [("Technical", tech), ("Communication", comm), ("Confidence", conf)]
    for col, (label, sc) in zip(cols, scores):
        sc_color = COLORS["success"] if sc >= 7 else (COLORS["warning"] if sc >= 5 else COLORS["danger"])
        with col:
            st.markdown(
                f"""<div style="background:{COLORS['bg_card']}; border-radius:10px; padding:1.25rem;
                    text-align:center; border:1px solid {COLORS['border']};">
                    <p style="color:{COLORS['text_muted']}; font-size:0.78rem; margin:0;">{label}</p>
                    <p style="color:{sc_color}; font-size:2rem; font-weight:700; margin:0.2rem 0;">
                        {sc}<span style="font-size:0.85rem; color:{COLORS['text_muted']};">/10</span></p>
                </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<h4 style='color:{COLORS['success']}; font-size:0.9rem;'>Strengths</h4>", unsafe_allow_html=True)
        for s in summary.get("strengths", []): st.markdown(f"- {s}")
    with c2:
        st.markdown(f"<h4 style='color:{COLORS['danger']}; font-size:0.9rem;'>Areas to Improve</h4>", unsafe_allow_html=True)
        for w in summary.get("weak_areas", []): st.markdown(f"- {w}")

    topics = summary.get("recommended_topics", [])
    if topics:
        st.markdown(f"<br><h4 style='color:{COLORS['accent']}; font-size:0.9rem;'>Recommended Study Topics</h4>", unsafe_allow_html=True)
        tags = " ".join(f'<span style="background:{COLORS["accent"]}15; color:{COLORS["accent"]}; padding:5px 14px; border-radius:4px; font-size:0.82rem; display:inline-block; margin:3px;">{t}</span>' for t in topics)
        st.markdown(tags, unsafe_allow_html=True)

    feedback = summary.get("detailed_feedback", "")
    if feedback:
        st.markdown(f"""<br><div style="background:{COLORS['bg_card']}; border-radius:10px; padding:1.25rem; border:1px solid {COLORS['border']};">
            <h4 style="color:{COLORS['text']}; margin:0 0 0.5rem 0; font-size:0.9rem;">Detailed Feedback</h4>
            <p style="color:{COLORS['text_secondary']}; font-size:0.88rem; line-height:1.7; margin:0;">{feedback}</p>
        </div>""", unsafe_allow_html=True)

    practice_qs = summary.get("suggested_questions_to_practice", [])
    if practice_qs:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Suggested Questions to Practice"):
            for i, q in enumerate(practice_qs, 1): st.markdown(f"**{i}.** {q}")

    with st.expander("Full Interview Transcript"):
        for msg in st.session_state.get("mock_conversation", []):
            role_label = {"interviewer": "Interviewer", "candidate": "You", "feedback": "Feedback"}.get(msg["role"], msg["role"])
            st.markdown(f"**{role_label}:** {msg['content']}")
            st.markdown("---")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("View Dashboard", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "Dashboard"
            st.rerun()
    with c2:
        if st.button("New Mock Interview", use_container_width=True):
            for key in ["mock_state", "mock_questions", "mock_evaluations", "mock_current_q", "mock_conversation", "mock_summary", "mock_completed"]:
                if key in st.session_state: del st.session_state[key]
            st.rerun()
