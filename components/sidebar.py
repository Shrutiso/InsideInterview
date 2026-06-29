"""
InsideInterview AI — Sidebar Component
"""

import streamlit as st
from config import COLORS


def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown(
            f"""
            <div style="text-align:center; padding: 1.25rem 0 0.75rem 0;">
                <h1 style="
                    color: {COLORS['primary_light']};
                    font-size: 1.35rem;
                    font-weight: 800;
                    margin: 0;
                    letter-spacing: -0.5px;
                ">InsideInterview</h1>
                <p style="color: {COLORS['text_muted']}; font-size: 0.7rem; margin-top: 2px;
                   letter-spacing: 2px; text-transform: uppercase;">
                    AI Interview Coach
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Navigation
        st.markdown(
            f"<p style='color:{COLORS['text_muted']}; font-size:0.65rem; "
            f"text-transform:uppercase; letter-spacing:2px; margin-bottom:0.5rem; font-weight: 600;'>"
            f"Navigation</p>",
            unsafe_allow_html=True,
        )

        pages = [
            ("Home", True),
            ("Assessment", bool(st.session_state.get("job_role"))),
            ("Resume Analysis", bool(st.session_state.get("level"))),
            ("Mock Interview", bool(st.session_state.get("resume_analysis"))),
            ("AI Coach", bool(st.session_state.get("job_role"))),
            ("Dashboard", bool(st.session_state.get("level"))),
            ("Session Logs", True),
        ]

        current_page = st.session_state.get("current_page", "Home")

        for page_name, unlocked in pages:
            if unlocked:
                if st.button(
                    page_name,
                    key=f"nav_{page_name}",
                    use_container_width=True,
                    type="primary" if current_page == page_name else "secondary",
                ):
                    st.session_state["current_page"] = page_name
                    st.rerun()
            else:
                st.button(
                    page_name,
                    key=f"nav_{page_name}",
                    use_container_width=True,
                    disabled=True,
                )

        st.markdown("---")

        # Session Progress
        if st.session_state.get("job_role"):
            st.markdown(
                f"<p style='color:{COLORS['text_muted']}; font-size:0.65rem; "
                f"text-transform:uppercase; letter-spacing:2px; margin-bottom:0.5rem; font-weight: 600;'>"
                f"Progress</p>",
                unsafe_allow_html=True,
            )

            steps = [
                ("Role Selected", bool(st.session_state.get("job_role"))),
                ("Assessment Done", bool(st.session_state.get("level"))),
                ("Resume Analyzed", bool(st.session_state.get("resume_analysis"))),
                ("Mock Interview", bool(st.session_state.get("mock_completed"))),
            ]

            completed = sum(1 for _, done in steps if done)
            st.progress(completed / len(steps))

            for step_name, done in steps:
                color = COLORS['success'] if done else COLORS['text_muted']
                marker = "+" if done else "-"
                st.markdown(
                    f"<p style='font-size:0.8rem; margin:3px 0; color: {color};'>"
                    f"{marker} {step_name}</p>",
                    unsafe_allow_html=True,
                )

            # Level badge
            if st.session_state.get("level"):
                level = st.session_state["level"]
                level_color = {
                    "Beginner": COLORS["warning"],
                    "Intermediate": COLORS["accent"],
                    "Advanced": COLORS["success"],
                }.get(level, COLORS["primary"])

                st.markdown(
                    f"""
                    <div style="
                        background: {COLORS['bg_card']};
                        border: 1px solid {level_color}40;
                        border-radius: 8px;
                        padding: 0.75rem;
                        margin-top: 0.75rem;
                        text-align: center;
                    ">
                        <p style="color: {level_color}; font-weight: 700; font-size: 0.85rem; margin: 0;">
                            {level}
                        </p>
                        <p style="color: {COLORS['text_muted']}; font-size: 0.7rem; margin: 2px 0 0 0;">
                            {st.session_state.get('job_role', '')}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("---")

        # API Key Settings
        st.markdown(
            f"<p style='color:{COLORS['text_muted']}; font-size:0.65rem; "
            f"text-transform:uppercase; letter-spacing:2px; margin-bottom:0.5rem; font-weight: 600;'>"
            f"API Key Settings</p>",
            unsafe_allow_html=True,
        )

        with st.expander("Configure Key", expanded=False):
            user_key = st.text_input(
                "Gemini API Key",
                key="custom_gemini_api_key",
                type="password",
                placeholder="AQ... or AIzaSy...",
                help="Google Gemini API Key from AI Studio. Both 'AQ.' (new) and 'AIzaSy' (old) key formats are supported."
            )

            if user_key:
                cleaned_key = user_key.strip()
                if cleaned_key != user_key:
                    st.session_state["custom_gemini_api_key"] = cleaned_key
                    st.rerun()

                if cleaned_key.startswith("AQ.") or cleaned_key.startswith("AIzaSy"):
                    st.success("Valid format detected! (AQ. or AIzaSy)")
                else:
                    st.warning("Warning: key should start with 'AQ.' or 'AIzaSy'.")

                if st.button("Reset to Default Key", use_container_width=True):
                    st.session_state["custom_gemini_api_key"] = ""
                    st.rerun()
            else:
                st.info("Using default system key.")

        st.markdown("---")

        # Reset
        if st.button("Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != "custom_gemini_api_key":
                    del st.session_state[key]
            st.session_state["current_page"] = "Home"
            st.rerun()
