import re
from collections import Counter
from .skills import SKILL_ALIASES

STOP_WORDS = {
    "the", "and", "for", "with", "you", "your", "our", "are", "will", "from",
    "this", "that", "have", "has", "who", "what", "when", "where", "into",
    "their", "they", "them", "about", "using", "use", "able", "ability",
    "work", "working", "role", "team", "years", "year", "experience", "skills",
    "strong", "good", "excellent", "knowledge", "required", "preferred",
    "responsibilities", "responsibility", "candidate", "job", "description",
    "development", "including", "such", "etc", "will", "must", "should",
}


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _contains_term(text: str, term: str) -> bool:
    escaped = re.escape(term.lower().strip())
    return bool(re.search(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", text))


def _job_keywords(job_text: str) -> list[str]:
    words = re.findall(r"[a-z][a-z0-9+#.-]{2,}", job_text.lower())
    counts = Counter(w.strip(".-") for w in words if w not in STOP_WORDS and len(w) > 2)
    return [word for word, _ in counts.most_common(18)]


def analyze_resume(resume_text: str, job_description: str) -> dict:
    resume = _normalise(resume_text)
    job = _normalise(job_description)

    job_skills = []
    resume_skills = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(_contains_term(job, alias) for alias in aliases):
            job_skills.append(canonical)
        if any(_contains_term(resume, alias) for alias in aliases):
            resume_skills.append(canonical)

    matched = sorted(set(job_skills) & set(resume_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    skill_coverage = len(matched) / max(1, len(job_skills))

    keywords = _job_keywords(job_description)
    matched_keywords = [word for word in keywords if _contains_term(resume, word)]
    keyword_coverage = len(matched_keywords) / max(1, len(keywords))

    sections = {
        "contact": bool(re.search(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}", resume)),
        "education": any(x in resume for x in ("education", "b.tech", "bachelor", "degree", "university", "college")),
        "experience": any(x in resume for x in ("experience", "internship", "employment", "work history")),
        "projects": "project" in resume,
    }
    section_score = sum(sections.values()) / len(sections)

    # Explainable heuristic: skill coverage 60%, job keyword overlap 25%, basic resume
    # section signals 15%. This is not a trained model or an ATS score.
    score = round(100 * (0.60 * skill_coverage + 0.25 * keyword_coverage + 0.15 * section_score))
    suggestions = []
    if missing:
        suggestions.append("If you genuinely have relevant experience with these skills, describe it clearly: " + ", ".join(missing[:6]) + ".")
    if not sections["projects"]:
        suggestions.append("Add a Projects section with outcomes, tools used, and your individual contribution.")
    if not sections["experience"]:
        suggestions.append("Add an Experience or Internship section. If you are early-career, include volunteering or relevant practical work.")
    if not sections["education"]:
        suggestions.append("Add an Education section with your qualification and institution.")
    if not sections["contact"]:
        suggestions.append("Include a professional contact email in the resume.")
    if not suggestions:
        suggestions.append("Your resume contains the main detected sections. Strengthen bullets with measurable outcomes and specific evidence.")

    return {
        "score": score,
        "score_label": "Strong alignment" if score >= 75 else "Moderate alignment" if score >= 50 else "Early alignment",
        "summary": f"Detected {len(matched)} of {len(job_skills)} job-related skills and {len(matched_keywords)} of {len(keywords)} selected job keywords.",
        "skills": {
            "required_detected": sorted(set(job_skills)),
            "matched": matched,
            "missing": missing,
            "resume_detected": sorted(set(resume_skills)),
        },
        "keywords": {
            "selected": keywords,
            "matched": matched_keywords,
            "coverage_percent": round(keyword_coverage * 100),
        },
        "sections": sections,
        "suggestions": suggestions,
        "methodology": "Heuristic text comparison only; not an ATS score, hiring recommendation, or prediction of job performance.",
    }
