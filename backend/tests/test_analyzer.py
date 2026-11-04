from app.analyzer import analyze_resume


RESUME = """
Alex Morgan
alex@example.com
EDUCATION
B.Tech Computer Science, Example University
PROJECTS
Built a React dashboard with Python FastAPI and SQL database.
EXPERIENCE
Software engineering internship. Used Git and Docker.
"""


def test_detects_matching_skills_and_sections():
    job = "We need Python, React, SQL, Docker and Git skills for a software engineering role."
    result = analyze_resume(RESUME, job)
    assert {"python", "react", "sql", "docker", "git"}.issubset(set(result["skills"]["matched"]))
    assert result["sections"]["contact"] is True
    assert result["sections"]["education"] is True
    assert result["sections"]["projects"] is True
    assert result["sections"]["experience"] is True
    assert 0 <= result["score"] <= 100


def test_missing_skills_are_reported():
    result = analyze_resume("Education: B.Tech. Projects: simple website.", "Need Python, Kubernetes and AWS.")
    assert "python" in result["skills"]["missing"]
    assert "aws" in result["skills"]["missing"]
    assert result["suggestions"]


def test_empty_job_does_not_crash():
    result = analyze_resume("Education and projects", "A sufficiently long job description with no listed technical terms.")
    assert isinstance(result["score"], int)
