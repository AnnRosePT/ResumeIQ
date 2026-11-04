# ResumeIQ — AI-Assisted Resume Analyzer

ResumeIQ is an original, GitHub-ready resume analysis platform built with **Python + FastAPI** and **React + Vite**. It extracts text from PDF/DOCX/TXT resumes, compares it with a job description, and returns an explainable match report.

> **Important:** ResumeIQ is a decision-support demo, not an automated hiring decision system. Its score is a transparent heuristic based on text overlap and section signals. It does not predict job performance, verify claims, or make hiring decisions. Review the original resume and assess candidates fairly.

## Features

- Upload PDF, DOCX, or TXT resumes (5 MB limit).
- Paste a job description and analyze the resume against it.
- Extract contact hints, skills, education, experience, and project signals.
- Explainable match score with matched and missing keywords.
- Actionable improvement suggestions.
- Sample resume and job description included.
- Responsive React dashboard with no external AI/API dependency.
- FastAPI validation, CORS configuration, and automated backend tests.

## Architecture

```text
resumeiq/
├── backend/       FastAPI API, parsing and analysis logic
├── frontend/      React + Vite dashboard
├── docs/          API and scoring documentation
├── sample-data/   Demo resume text and job description
└── .github/       Issue and pull request templates
```

## Quick start

### Requirements
- Python 3.10+
- Node.js 18+
- npm

### 1. Start the backend

```bash
cd backend
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (usually http://localhost:5173).

The frontend proxies `/api` requests to `http://localhost:8000`.

## Run tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

## Try the sample

1. Open `sample-data/sample_resume.txt`.
2. Paste its content into a `.txt` file if needed, or upload the supplied file.
3. Copy `sample-data/sample_job_description.txt` into the job-description field.
4. Click **Analyze resume**.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/analyze` | Upload resume + job description and return report |

See [`docs/API.md`](docs/API.md) and [`docs/SCORING.md`](docs/SCORING.md).

## Configuration

Copy `backend/.env.example` to `backend/.env` if you need to change settings. Set `FRONTEND_ORIGIN` to your deployed frontend origin before production deployment.

## Privacy and security

- Uploaded file content is processed in memory and is not saved to disk by this demo.
- Do not upload sensitive personal documents to an untrusted deployment.
- This demo has no authentication, rate limiting, malware scanning, or persistent audit controls. Add these before public production use.
- Do not use protected attributes (age, gender, ethnicity, religion, disability, etc.) in screening decisions.
- Treat extracted information as unverified and allow candidates to correct errors.

## Known limitations

- PDF extraction works best with text-based PDFs. Scanned PDFs require OCR, which is intentionally not included.
- DOCX tables and complex layouts may not preserve reading order.
- Skill matching uses a small editable dictionary in `backend/app/skills.py`; tune it for your domain.
- The score is not an ATS score and should not be represented as one.

## License

MIT — see [`LICENSE`](LICENSE).
