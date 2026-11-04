# Scoring methodology

ResumeIQ uses a deliberately simple and inspectable heuristic. It is **not** a trained machine-learning model, an ATS score, a candidate-quality rating, or a hiring recommendation.

The score is calculated as:

- **60% skill coverage:** detected job skills also found in resume text / detected job skills.
- **25% selected keyword overlap:** selected non-stopword job-description terms found in resume text / selected terms.
- **15% section signals:** presence of contact email, education, experience, and projects sections.

The weighted result is rounded to an integer from 0 to 100. If no skills or keywords are detected, the denominator is protected to avoid division by zero.

## Interpretation

- 75–100: Strong alignment (text signals only)
- 50–74: Moderate alignment (text signals only)
- 0–49: Early alignment (text signals only)

A missing keyword does not prove a candidate lacks that skill. They may use different terminology or have omitted relevant evidence. A detected keyword does not verify proficiency. Review context, portfolio evidence, and candidate-provided corrections.

## Customization

Edit `backend/app/skills.py` to add domain-specific skills and aliases. Keep the vocabulary job-related, document changes, and validate matching behavior with tests.
