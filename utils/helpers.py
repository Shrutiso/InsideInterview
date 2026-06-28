"""
InsideInterview AI — Helper Utilities
Scoring, level classification, session management, and formatting.
"""

import json
from datetime import datetime
from config import LEVEL_THRESHOLDS


def classify_level(score: int, total: int = 20) -> str:
    """Classify candidate level based on assessment score."""
    if score >= LEVEL_THRESHOLDS["Advanced"]:
        return "Advanced"
    elif score >= LEVEL_THRESHOLDS["Intermediate"]:
        return "Intermediate"
    else:
        return "Beginner"


def calculate_section_scores(answers: dict, assessment_data: dict) -> dict:
    """
    Calculate scores per section.
    Returns dict with section names and their scores.
    """
    section_scores = {}
    for section in assessment_data.get("sections", []):
        section_name = section["name"]
        correct = 0
        total = len(section["questions"])
        for q in section["questions"]:
            q_id = str(q["id"])
            if q_id in answers and answers[q_id] == q["correct_answer"]:
                correct += 1
        section_scores[section_name] = {
            "correct": correct,
            "total": total,
            "percentage": round((correct / total) * 100, 1) if total > 0 else 0,
        }
    return section_scores


def calculate_total_score(answers: dict, assessment_data: dict) -> int:
    """Calculate total correct answers across all sections."""
    total = 0
    for section in assessment_data.get("sections", []):
        for q in section["questions"]:
            q_id = str(q["id"])
            if q_id in answers and answers[q_id] == q["correct_answer"]:
                total += 1
    return total


def format_timestamp() -> str:
    """Return current timestamp as formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_session_log(session_state) -> dict:
    """Create a comprehensive session log from session state."""
    log = {
        "timestamp": format_timestamp(),
        "job_role": session_state.get("job_role", "Not selected"),
        "level": session_state.get("level", "Not assessed"),
        "assessment_score": session_state.get("assessment_score", 0),
        "section_scores": session_state.get("section_scores", {}),
        "resume_uploaded": session_state.get("resume_text", "") != "",
        "resume_score": None,
        "mock_interview_completed": session_state.get("mock_completed", False),
        "chat_history": session_state.get("coach_history", []),
    }

    # Add resume analysis data if available
    if session_state.get("resume_analysis"):
        ra = session_state["resume_analysis"]
        log["resume_score"] = ra.get("resume_score", 0)
        log["skills"] = ra.get("skills", [])
        log["strengths"] = ra.get("strengths", [])
        log["weaknesses"] = ra.get("weaknesses", [])
        log["missing_skills"] = ra.get("missing_skills", [])

    # Add mock interview data if available
    if session_state.get("mock_summary"):
        ms = session_state["mock_summary"]
        log["mock_interview"] = {
            "technical_score": ms.get("overall_technical_score", 0),
            "communication_score": ms.get("overall_communication_score", 0),
            "confidence_score": ms.get("overall_confidence_score", 0),
            "overall_rating": ms.get("overall_rating", "N/A"),
        }

    return log


def session_log_to_text(log: dict) -> str:
    """Convert session log dict to a readable text format."""
    lines = [
        "=" * 60,
        "  INSIDEINTERVIEW AI — SESSION REPORT",
        "=" * 60,
        f"  Date: {log['timestamp']}",
        f"  Target Role: {log['job_role']}",
        f"  Candidate Level: {log['level']}",
        "",
        "─" * 60,
        "  ASSESSMENT RESULTS",
        "─" * 60,
        f"  Total Score: {log['assessment_score']}/20",
    ]

    for section_name, scores in log.get("section_scores", {}).items():
        lines.append(f"    {section_name}: {scores['correct']}/{scores['total']} ({scores['percentage']}%)")

    if log.get("resume_score") is not None:
        lines.extend([
            "",
            "─" * 60,
            "  RESUME ANALYSIS",
            "─" * 60,
            f"  Resume Score: {log['resume_score']}/100",
            f"  Skills: {', '.join(log.get('skills', []))}",
            f"  Strengths: {', '.join(log.get('strengths', []))}",
            f"  Weaknesses: {', '.join(log.get('weaknesses', []))}",
            f"  Missing Skills: {', '.join(log.get('missing_skills', []))}",
        ])

    if log.get("mock_interview"):
        mi = log["mock_interview"]
        lines.extend([
            "",
            "─" * 60,
            "  MOCK INTERVIEW RESULTS",
            "─" * 60,
            f"  Technical Score: {mi['technical_score']}/10",
            f"  Communication Score: {mi['communication_score']}/10",
            f"  Confidence Score: {mi['confidence_score']}/10",
            f"  Overall Rating: {mi['overall_rating']}",
        ])

    lines.extend([
        "",
        "=" * 60,
        "  END OF REPORT",
        "=" * 60,
    ])

    return "\n".join(lines)


def get_level_emoji(level: str) -> str:
    """Return emoji for candidate level."""
    return {
        "Beginner": "🌱",
        "Intermediate": "🌿",
        "Advanced": "🌳",
    }.get(level, "📊")


def get_score_color(score: float, max_score: float = 100) -> str:
    """Return a color based on score percentage."""
    pct = (score / max_score) * 100 if max_score > 0 else 0
    if pct >= 80:
        return "#00E676"
    elif pct >= 60:
        return "#FFD600"
    elif pct >= 40:
        return "#FF9100"
    else:
        return "#FF5252"
