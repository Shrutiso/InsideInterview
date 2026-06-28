"""
InsideInterview AI — Session Logs Component
"""

import json
import streamlit as st
from config import COLORS
from utils.helpers import create_session_log, session_log_to_text, format_timestamp


def render_session_logs():
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1 style="color: {COLORS['text']}; font-size: 2rem; font-weight: 800;">Session Logs</h1>
            <p style="color: {COLORS['text_muted']}; font-size: 0.95rem;">
                Complete history of your interview preparation session
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    logs = st.session_state.get("session_logs", [])
    job_role = st.session_state.get("job_role", "Not selected")
    level = st.session_state.get("level", "Not assessed")
    score = st.session_state.get("assessment_score", 0)
    resume_analysis = st.session_state.get("resume_analysis")

    # Session Summary
    st.markdown(
        f"""
        <div style="background:{COLORS['bg_card']}; border:1px solid {COLORS['border']};
            border-radius:12px; padding:1.5rem; margin-bottom:1.5rem;">
            <h3 style="color:{COLORS['text']}; margin:0 0 1rem 0; font-size:1.05rem;">Session Summary</h3>
            <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:0.75rem;">
                <div><p style="color:{COLORS['text_muted']}; font-size:0.7rem; margin:0;">Target Role</p>
                    <p style="color:{COLORS['primary_light']}; font-weight:600; margin:0;">{job_role}</p></div>
                <div><p style="color:{COLORS['text_muted']}; font-size:0.7rem; margin:0;">Level</p>
                    <p style="color:{COLORS['accent']}; font-weight:600; margin:0;">{level}</p></div>
                <div><p style="color:{COLORS['text_muted']}; font-size:0.7rem; margin:0;">Assessment</p>
                    <p style="color:{COLORS['text']}; font-weight:600; margin:0;">{score}/20</p></div>
                <div><p style="color:{COLORS['text_muted']}; font-size:0.7rem; margin:0;">Resume Score</p>
                    <p style="color:{COLORS['text']}; font-weight:600; margin:0;">{resume_analysis.get('resume_score', '--') if resume_analysis else '--'}/100</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Activity Timeline
    st.markdown(f"<h3 style='color:{COLORS['text']}; font-size:1rem;'>Activity Timeline</h3>", unsafe_allow_html=True)

    if logs:
        event_colors = {
            "Assessment Completed": COLORS["primary"],
            "Resume Analyzed": COLORS["accent"],
            "Mock Interview Started": COLORS["warning"],
            "Mock Interview Completed": COLORS["success"],
            "Coach Interaction": COLORS["primary_light"],
        }
        for i, entry in enumerate(reversed(logs)):
            event = entry.get("event", "Unknown")
            color = event_colors.get(event, COLORS["text_muted"])
            details = []
            for k, v in entry.items():
                if k != "event":
                    if isinstance(v, dict): details.append(f"{k}: {json.dumps(v)}")
                    elif isinstance(v, str) and len(v) > 100: details.append(f"{k}: {v[:100]}...")
                    else: details.append(f"{k}: {v}")
            detail_text = " | ".join(details) if details else ""

            st.markdown(
                f"""<div style="background:{COLORS['bg_card']}; border-left:3px solid {color};
                    border-radius:0 6px 6px 0; padding:0.65rem 1rem; margin:0.3rem 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <p style="color:{COLORS['text']}; font-weight:600; font-size:0.85rem; margin:0;">{event}</p>
                        <span style="color:{COLORS['text_muted']}; font-size:0.6rem; background:{COLORS['bg_card']};
                            padding:2px 8px; border-radius:4px; border:1px solid {COLORS['border']};">#{len(logs) - i}</span>
                    </div>
                    <p style="color:{COLORS['text_muted']}; font-size:0.72rem; margin:0.1rem 0 0 0;">{detail_text}</p>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No activity recorded yet. Start by selecting a job role.")

    # Chat & Interview logs
    coach_history = st.session_state.get("coach_history", [])
    if coach_history:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"AI Coach Conversation ({len(coach_history)} messages)"):
            for msg in coach_history:
                role = "You" if msg["role"] == "user" else "Coach"
                st.markdown(f"**{role}:** {msg['content']}")
                st.markdown("---")

    mock_conv = st.session_state.get("mock_conversation", [])
    if mock_conv:
        with st.expander(f"Mock Interview Transcript ({len(mock_conv)} exchanges)"):
            for msg in mock_conv:
                role = {"interviewer": "Interviewer", "candidate": "You", "feedback": "Feedback"}.get(msg.get("role", ""), "")
                st.markdown(f"**{role}:** {msg.get('content', '')}")
                st.markdown("---")

    # Downloads
    st.markdown(f"<br><h3 style='color:{COLORS['text']}; font-size:1rem;'>Download Report</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    session_log = create_session_log(st.session_state)
    with c1:
        st.download_button("Download Text Report", data=session_log_to_text(session_log),
            file_name=f"insideinterview_report_{format_timestamp().replace(' ', '_').replace(':', '-')}.txt",
            mime="text/plain", use_container_width=True)
    with c2:
        st.download_button("Download JSON Report", data=json.dumps(session_log, indent=2, default=str),
            file_name=f"insideinterview_report_{format_timestamp().replace(' ', '_').replace(':', '-')}.json",
            mime="application/json", use_container_width=True)
