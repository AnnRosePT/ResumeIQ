# API reference

Base URL (local): `http://localhost:8000`

## `GET /api/health`

Returns service health and version.

## `POST /api/analyze`

Content type: `multipart/form-data`

| Field | Type | Required | Notes |
|---|---|---|---|
| `resume` | file | Yes | `.pdf`, `.docx`, or `.txt`; maximum 5 MB by default |
| `job_description` | string | Yes | 40–20,000 characters |

Example using curl:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "resume=@../sample-data/sample_resume.txt" \
  -F "job_description=We need Python, React, SQL and Git developers with project experience."
```

Success response (abridged):

```json
{
  "filename": "sample_resume.txt",
  "characters_analyzed": 620,
  "report": {
    "score": 72,
    "score_label": "Moderate alignment",
    "skills": {
      "matched": ["python", "react"],
      "missing": ["aws"]
    },
    "suggestions": []
  }
}
```

Errors: `400` unreadable file, `413` size/description limit, `415` unsupported file extension, `422` invalid job description.
