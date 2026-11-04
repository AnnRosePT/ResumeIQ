from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rejects_unsupported_file():
    response = client.post(
        "/api/analyze",
        data={"job_description": "This is a sufficiently long job description for testing purposes."},
        files={"resume": ("resume.exe", b"not a resume", "application/octet-stream")},
    )
    assert response.status_code == 415


def test_rejects_short_job_description():
    response = client.post(
        "/api/analyze",
        data={"job_description": "Too short"},
        files={"resume": ("resume.txt", b"This is a sufficiently long sample resume text with education and projects.", "text/plain")},
    )
    assert response.status_code == 422
