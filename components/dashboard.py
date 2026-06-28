"""
InsideInterview AI — Dashboard Component
"""

import streamlit as st
import plotly.graph_objects as go
from config import COLORS
from utils.helpers import get_score_color


def render_dashboard():
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1 style="color: {COLORS['text']}; font-size: 2rem; font-weight: 800;">Performance Dashboard</h1>
            <p style="color: {COLORS['text_muted']}; font-size: 0.95rem;">Your complete interview readiness overview</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.get("level"):
        st.info("Complete the assessment to see your dashboard.")
        return

    job_role = st.session_state.get("job_role", "")
    level = st.session_state.get("level", "")
    score = st.session_state.get("assessment_score", 0)
    section_scores = st.session_state.get("section_scores", {})
    resume_analysis = st.session_state.get("resume_analysis")
    mock_summary = st.session_state.get("mock_summary")

    level_color = {"Beginner": COLORS["warning"], "Intermediate": COLORS["accent"], "Advanced": COLORS["success"]}.get(level, COLORS["primary"])

    # Top Metrics
    m_cols = st.columns(4)
    metrics = [
        ("Target Role", job_role, COLORS["primary_light"]),
        ("Your Level", level, level_color),
        ("Assessment", f"{score}/20", get_score_color(score, 20)),
        ("Resume Score", f"{resume_analysis.get('resume_score', '--')}/100" if resume_analysis else "--", get_score_color(resume_analysis.get("resume_score", 0), 100) if resume_analysis else COLORS["text_muted"]),
    ]
    for col, (label, value, color) in zip(m_cols, metrics):
        with col:
            st.markdown(
                f"""<div style="background:{COLORS['bg_card']}; border-radius:10px; padding:1.15rem;
                    text-align:center; border:1px solid {COLORS['border']};">
                    <p style="color:{COLORS['text_muted']}; font-size:0.65rem; margin:0; text-transform:uppercase; letter-spacing:1px;">{label}</p>
                    <p style="color:{color}; font-size:1.05rem; font-weight:700; margin:0.2rem 0 0 0;">{value}</p>
                </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown(f"<h3 style='color:{COLORS['text']}; font-size:1rem;'>Assessment Breakdown</h3>", unsafe_allow_html=True)
        if section_scores:
            sections = list(section_scores.keys())
            percentages = [section_scores[s]["percentage"] for s in sections]
            bar_colors = [COLORS["success"] if p >= 80 else (COLORS["warning"] if p >= 50 else COLORS["danger"]) for p in percentages]

            fig = go.Figure(data=[go.Bar(x=sections, y=percentages, marker_color=bar_colors,
                text=[f"{p}%" for p in percentages], textposition="outside",
                textfont=dict(color=COLORS["text"], size=12))])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=COLORS["text_muted"]),
                yaxis=dict(range=[0, 110], title="Score %", gridcolor="#1E293B"),
                xaxis=dict(title=""), margin=dict(l=40, r=20, t=20, b=40), height=300)
            st.plotly_chart(fig, use_container_width=True)

    with ch2:
        if mock_summary:
            st.markdown(f"<h3 style='color:{COLORS['text']}; font-size:1rem;'>Interview Scores</h3>", unsafe_allow_html=True)
            categories = ["Technical", "Communication", "Confidence"]
            values = [mock_summary.get("overall_technical_score", 0), mock_summary.get("overall_communication_score", 0), mock_summary.get("overall_confidence_score", 0)]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]],
                fill="toself", fillcolor="rgba(79,70,229,0.15)", line=dict(color=COLORS["primary"], width=2),
                marker=dict(size=7, color=COLORS["primary"])))
            fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 10], gridcolor="#1E293B", tickfont=dict(color=COLORS["text_muted"])),
                angularaxis=dict(gridcolor="#1E293B", tickfont=dict(color=COLORS["text"], size=11))),
                paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=60, r=60, t=30, b=30), height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(f"<h3 style='color:{COLORS['text']}; font-size:1rem;'>Interview Scores</h3>", unsafe_allow_html=True)
            st.info("Complete a mock interview to see your scores here.")

    # Readiness Gauge
    st.markdown(f"<br><h3 style='color:{COLORS['text']}; font-size:1rem;'>Interview Readiness</h3>", unsafe_allow_html=True)
    readiness = _calculate_readiness(score, resume_analysis, mock_summary)
    r_color = get_score_color(readiness, 100)

    fig = go.Figure(go.Indicator(mode="gauge+number", value=readiness,
        number=dict(suffix="%", font=dict(size=36, color=COLORS["text"])),
        gauge=dict(axis=dict(range=[0, 100], tickcolor=COLORS["text_muted"]),
            bar=dict(color=r_color), bgcolor="#1E293B", borderwidth=0,
            steps=[dict(range=[0, 40], color="rgba(239,68,68,0.1)"),
                dict(range=[40, 70], color="rgba(245,158,11,0.1)"),
                dict(range=[70, 100], color="rgba(16,185,129,0.1)")])))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text_muted"]),
        height=240, margin=dict(l=30, r=30, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # Strengths & Weaknesses
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f"<h3 style='color:{COLORS['success']}; font-size:1rem;'>Your Strengths</h3>", unsafe_allow_html=True)
        all_s = set()
        if resume_analysis: all_s.update(resume_analysis.get("strengths", []))
        if mock_summary: all_s.update(mock_summary.get("strengths", []))
        for n, sc in section_scores.items():
            if sc["percentage"] >= 80: all_s.add(f"Strong {n} skills ({sc['percentage']}%)")
        for s in all_s: st.markdown(f"- {s}")
        if not all_s: st.info("Complete more sections to identify strengths.")

    with s2:
        st.markdown(f"<h3 style='color:{COLORS['danger']}; font-size:1rem;'>Areas to Improve</h3>", unsafe_allow_html=True)
        all_w = set()
        if resume_analysis: all_w.update(resume_analysis.get("weaknesses", [])); all_w.update(resume_analysis.get("missing_skills", []))
        if mock_summary: all_w.update(mock_summary.get("weak_areas", []))
        for n, sc in section_scores.items():
            if sc["percentage"] < 50: all_w.add(f"Needs improvement in {n} ({sc['percentage']}%)")
        for w in all_w: st.markdown(f"- {w}")
        if not all_w: st.info("Complete more sections to identify areas for improvement.")


def _calculate_readiness(assessment_score, resume_analysis, mock_summary):
    total_weight = 0
    weighted_score = 0
    assessment_pct = (assessment_score / 20) * 100
    weighted_score += assessment_pct * 0.30
    total_weight += 0.30
    if resume_analysis:
        weighted_score += resume_analysis.get("resume_score", 0) * 0.30
        total_weight += 0.30
    if mock_summary:
        tech = mock_summary.get("overall_technical_score", 0)
        comm = mock_summary.get("overall_communication_score", 0)
        conf = mock_summary.get("overall_confidence_score", 0)
        weighted_score += ((tech + comm + conf) / 30) * 100 * 0.40
        total_weight += 0.40
    return round(weighted_score / total_weight, 1) if total_weight > 0 else 0
