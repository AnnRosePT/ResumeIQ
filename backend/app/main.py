import os
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .analyzer import analyze_resume
from .parser import extract_text, ResumeParseError

MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "5")) * 1024 * 1024
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

app = FastAPI(
    title="ResumeIQ API",
    description="Explainable resume-to-job-description text analysis demo.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ResumeIQ API", "version": "1.0.0"}


@app.post("/api/analyze")
async def analyze(
    job_description: str = Form(...),
    resume: UploadFile = File(...),
):
    if not job_description.strip() or len(job_description.strip()) < 40:
        raise HTTPException(status_code=422, detail="Please provide a job description with at least 40 characters.")
    if len(job_description) > 20_000:
        raise HTTPException(status_code=413, detail="Job description is too long (20,000 character limit).")

    filename = resume.filename or "resume.txt"
    if not filename.lower().endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(status_code=415, detail="Unsupported file type. Upload PDF, DOCX, or TXT.")

    content = await resume.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"File exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB upload limit.")

    try:
        resume_text = extract_text(filename, content)
    except ResumeParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    report = analyze_resume(resume_text, job_description)
    return {
        "filename": filename,
        "characters_analyzed": len(resume_text),
        "report": report,
    }
