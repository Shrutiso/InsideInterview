"""
InsideInterview AI — AI Coach Chat Component
"""

import streamlit as st
from config import COLORS
from utils.gemini_client import coach_chat


def render_chat_coach():
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1 style="color: {COLORS['text']}; font-size: 2rem; font-weight: 800;">AI Interview Coach</h1>
            <p style="color: {COLORS['text_muted']}; font-size: 0.95rem;">
                Ask anything about interview preparation -- personalized to your profile
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "coach_history" not in st.session_state:
        st.session_state["coach_history"] = []

    job_role = st.session_state.get("job_role", "Not selected")
    level = st.session_state.get("level", "Not assessed")

    # Context Banner
    st.markdown(
        f"""
        <div style="background:{COLORS['bg_card']}; border:1px solid {COLORS['border']};
            border-radius:8px; padding:0.65rem 1.25rem; margin-bottom:1.5rem;
            display:flex; gap:2rem; align-items:center;">
            <div>
                <span style="color:{COLORS['text_muted']}; font-size:0.65rem; text-transform:uppercase; letter-spacing:1px;">Role</span><br>
                <span style="color:{COLORS['primary_light']}; font-weight:600; font-size:0.82rem;">{job_role}</span>
            </div>
            <div>
                <span style="color:{COLORS['text_muted']}; font-size:0.65rem; text-transform:uppercase; letter-spacing:1px;">Level</span><br>
                <span style="color:{COLORS['accent']}; font-weight:600; font-size:0.82rem;">{level}</span>
            </div>
            <div style="flex:1; text-align:right;">
                <span style="color:{COLORS['text_muted']}; font-size:0.7rem;">
                    Context from your assessment, resume, and interview is active
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Actions
    st.markdown(f"<p style='color:{COLORS['text_muted']}; font-size:0.72rem; margin-bottom:0.4rem;'>Quick Questions:</p>", unsafe_allow_html=True)
    qcols = st.columns(4)
    quick_prompts = [
        "How should I prepare for my role?",
        "Explain my weak areas in detail",
        "Give me practice questions",
        "Create a study plan for me",
    ]
    for col, prompt in zip(qcols, quick_prompts):
        with col:
            if st.button(prompt.split("?")[0] if "?" in prompt else prompt[:25], key=f"quick_{prompt}", use_container_width=True):
                _send_message(prompt)

    st.markdown("---")

    # Chat History
    if not st.session_state["coach_history"]:
        st.markdown(
            f"""<div style="text-align:center; padding:3rem 1rem; color:{COLORS['text_muted']};">
                <p style="font-size:1rem; font-weight:500; margin:0.5rem 0;">
                    Hi, I am your AI Interview Coach.</p>
                <p style="font-size:0.82rem; margin:0;">
                    I have context from your target role, skill level, resume, and interview performance.<br>
                    Ask me anything about interview preparation.</p>
            </div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state["coach_history"]:
            if msg["role"] == "user":
                st.markdown(
                    f"""<div style="background:rgba(79,70,229,0.08); border-right:3px solid {COLORS['primary']};
                        border-radius:10px 0 0 10px; padding:0.7rem 1.2rem; margin:0.4rem 0 0.4rem 3rem;">
                        <p style="color:{COLORS['primary_light']}; font-weight:600; font-size:0.65rem; margin:0 0 0.2rem 0;
                            text-transform:uppercase; letter-spacing:1px;">You</p>
                        <p style="color:{COLORS['text']}; font-size:0.88rem; margin:0; line-height:1.6;">{msg['content']}</p>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""<div style="background:{COLORS['bg_card']}; border-left:3px solid {COLORS['accent']};
                        border-radius:0 10px 10px 0; padding:0.7rem 1.2rem; margin:0.4rem 3rem 0.4rem 0;">
                        <p style="color:{COLORS['accent']}; font-weight:600; font-size:0.65rem; margin:0 0 0.2rem 0;
                            text-transform:uppercase; letter-spacing:1px;">AI Coach</p>
                    </div>""", unsafe_allow_html=True)
                st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask me anything about interview preparation...")
    if user_input:
        _send_message(user_input)

    if st.session_state["coach_history"]:
        if st.button("Clear Chat", key="clear_coach"):
            st.session_state["coach_history"] = []
            st.rerun()


def _send_message(message):
    job_role = st.session_state.get("job_role", "Not selected")
    level = st.session_state.get("level", "Not assessed")
    score = st.session_state.get("assessment_score", 0)
    ra = st.session_state.get("resume_analysis", {})
    skills = ra.get("skills", []) if ra else []
    weak_areas = []
    if ra:
        weak_areas.extend(ra.get("weaknesses", []))
        weak_areas.extend(ra.get("missing_skills", []))

    st.session_state["coach_history"].append({"role": "user", "content": message})

    with st.spinner("Thinking..."):
        try:
            response = coach_chat(job_role=job_role, level=level, score=score, skills=skills,
                weak_areas=weak_areas[:5], chat_history=st.session_state["coach_history"], user_message=message)
        except Exception as e:
            st.error(f"Coach error: {str(e)}")
            # Pop user message if failed so history stays clean
            st.session_state["coach_history"].pop()
            return

    st.session_state["coach_history"].append({"role": "assistant", "content": response})

    if "session_logs" not in st.session_state: st.session_state["session_logs"] = []
    st.session_state["session_logs"].append({"event": "Coach Interaction", "user_message": message[:100]})
    st.rerun()
