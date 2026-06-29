"""
InsideInterview AI — Google Gemini API Client
"""

import time
import json
import re
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import streamlit as st
from config import (
    GEMINI_API_KEY,
    ASSESSMENT_PROMPT,
    RESUME_ANALYSIS_PROMPT,
    MOCK_INTERVIEW_START_PROMPT,
    MOCK_INTERVIEW_EVALUATE_PROMPT,
    MOCK_INTERVIEW_SUMMARY_PROMPT,
    COACH_SYSTEM_PROMPT,
)

# ─── SDK Setup ───────────────────────────────────────────────
_client = None
_sdk_mode = None
_last_initialized_key = None

# Models to try in order — if one hits quota, fall back to the next
_MODEL_FALLBACKS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]


def _get_active_api_key():
    """Get the active API key, prioritizing session state overrides."""
    if st.session_state.get("custom_gemini_api_key"):
        return st.session_state["custom_gemini_api_key"].strip()
    return GEMINI_API_KEY


def _init_sdk():
    """Initialize the Gemini SDK (runs on startup or key change)."""
    global _client, _sdk_mode, _last_initialized_key

    active_key = _get_active_api_key()

    if _sdk_mode is not None and _last_initialized_key == active_key:
        return

    # Clear previous clients if key changed
    _client = None
    _sdk_mode = None

    # Attempt 1: google-genai (newer SDK, uses Client)
    try:
        from google import genai as genai_new
        _client = genai_new.Client(api_key=active_key)
        _sdk_mode = "genai_client"
        _last_initialized_key = active_key
        return
    except (ImportError, AttributeError):
        pass

    # Attempt 2: google-generativeai (older SDK)
    try:
        import google.generativeai as genai_old
        genai_old.configure(api_key=active_key)
        _client = genai_old
        _sdk_mode = "generativeai"
        _last_initialized_key = active_key
        return
    except (ImportError, Exception) as e:
        raise ImportError(
            "Could not import a Gemini SDK. "
            "Install either 'google-genai' or 'google-generativeai'. "
            f"Error: {e}"
        )


def _generate_with_model(model_name, prompt):
    """Generate content using a specific model."""
    if _sdk_mode == "genai_client":
        response = _client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    else:
        model = _client.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text


def _generate_content(prompt, max_retries=3, initial_delay=5.0):
    """
    Generate content with model fallback and retry logic.
    Tries each model in _MODEL_FALLBACKS. If a model hits quota/rate limits,
    moves to the next model. Retries transient errors with backoff.
    """
    _init_sdk()

    last_error = None

    for model_name in _MODEL_FALLBACKS:
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return _generate_with_model(model_name, prompt)

            except Exception as e:
                last_error = e
                err_str = str(e).lower()

                is_quota_error = any(
                    kw in err_str
                    for kw in ("exhausted", "429", "quota", "resource_exhausted")
                )

                if is_quota_error:
                    if attempt == 0:
                        # First attempt failed with quota — try next model immediately
                        break
                    # Subsequent attempts — wait and retry
                    time.sleep(delay)
                    delay *= 2
                    continue

                is_transient = any(
                    kw in err_str
                    for kw in ("503", "500", "unavailable", "internal", "timeout")
                )
                if is_transient and attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue

                # Non-retryable error — raise immediately
                raise e

    # All models exhausted or key invalid
    error_msg = str(last_error)
    err_str = error_msg.lower()

    is_quota_error = any(
        kw in err_str
        for kw in ("exhausted", "429", "quota", "resource_exhausted")
    )

    is_key_invalid = any(
        kw in err_str
        for kw in ("key_invalid", "api key invalid", "invalid key", "api_key_invalid", "unauthorized", "api key not valid", "400")
    )

    if is_quota_error:
        raise RuntimeError(
            "⚠️ Gemini API quota exhausted for ALL models.\n"
            "This means your API key has hit its rate limit.\n\n"
            "**To fix this:**\n"
            "1. Go to the sidebar under **API Key Settings**.\n"
            "2. Paste a new Gemini API key (starts with 'AQ.' or 'AIzaSy').\n"
            "3. Or wait 1-2 minutes for the rate limit to reset.\n\n"
            f"Original error: {error_msg}"
        )
    elif is_key_invalid:
        raise RuntimeError(
            "⚠️ Invalid Gemini API Key.\n\n"
            "**To fix this:**\n"
            "1. Go to https://aistudio.google.com/apikey\n"
            "2. Generate a NEW API key (starts with 'AQ.' or 'AIzaSy').\n"
            "3. Paste it in the sidebar under **API Key Settings**.\n\n"
            f"Original error: {error_msg}"
        )
    raise last_error


def _parse_json_response(text: str) -> dict:
    """Extract and parse JSON from a Gemini response."""
    if text is None:
        return None

    # Try markdown code blocks first
    patterns = [
        r"```json\s*([\s\S]*?)\s*```",
        r"```\s*([\s\S]*?)\s*```",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    # Try raw JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON object
    brace_start = text.find("{")
    brace_end = text.rfind("}") + 1
    if brace_start != -1 and brace_end > brace_start:
        try:
            return json.loads(text[brace_start:brace_end])
        except json.JSONDecodeError:
            pass

    return None


def generate_assessment(job_role: str) -> dict:
    prompt = ASSESSMENT_PROMPT.format(job_role=job_role)
    response_text = _generate_content(prompt)
    result = _parse_json_response(response_text)
    if result is None:
        response_text = _generate_content(prompt + "\n\nIMPORTANT: Return ONLY valid JSON.")
        result = _parse_json_response(response_text)
    return result


def analyze_resume(job_role: str, level: str, resume_text: str) -> dict:
    prompt = RESUME_ANALYSIS_PROMPT.format(job_role=job_role, level=level, resume_text=resume_text)
    response_text = _generate_content(prompt)
    result = _parse_json_response(response_text)
    if result is None:
        response_text = _generate_content(prompt + "\n\nIMPORTANT: Return ONLY valid JSON.")
        result = _parse_json_response(response_text)
    return result


def start_mock_interview(job_role: str, level: str, score: int, skills: list, weak_areas: list) -> dict:
    prompt = MOCK_INTERVIEW_START_PROMPT.format(
        job_role=job_role, level=level, score=score,
        skills=", ".join(skills) if skills else "Not provided",
        weak_areas=", ".join(weak_areas) if weak_areas else "Not identified yet",
    )
    response_text = _generate_content(prompt)
    return _parse_json_response(response_text)


def evaluate_mock_answer(job_role, level, question_number, question, expected_points, answer):
    prompt = MOCK_INTERVIEW_EVALUATE_PROMPT.format(
        job_role=job_role, level=level, question_number=question_number,
        question=question, expected_points=", ".join(expected_points),
        answer=answer, next_number=question_number + 1,
    )
    response_text = _generate_content(prompt)
    return _parse_json_response(response_text)


def generate_interview_summary(job_role: str, evaluations: list) -> dict:
    prompt = MOCK_INTERVIEW_SUMMARY_PROMPT.format(
        job_role=job_role, evaluations=json.dumps(evaluations, indent=2),
    )
    response_text = _generate_content(prompt)
    return _parse_json_response(response_text)


def coach_chat(job_role, level, score, skills, weak_areas, chat_history, user_message):
    system_context = COACH_SYSTEM_PROMPT.format(
        job_role=job_role, level=level, score=score,
        skills=", ".join(skills) if skills else "Not provided",
        weak_areas=", ".join(weak_areas) if weak_areas else "Not identified yet",
    )
    history_text = ""
    for msg in chat_history[-10:]:
        role = "Candidate" if msg["role"] == "user" else "Coach"
        history_text += f"\n{role}: {msg['content']}"
    full_prompt = f"""{system_context}\n\n**Conversation History:**\n{history_text}\n\n**Candidate's New Message:** {user_message}\n\nRespond as the AI Coach. Be helpful, specific, and personalized."""
    response_text = _generate_content(full_prompt)
    return response_text
