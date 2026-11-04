# Privacy, safety, and fair use

ResumeIQ is a local educational prototype.

- File bytes are read into memory and are not persisted by the API code.
- Avoid logging resume text or returning extracted personal information unnecessarily.
- A production deployment should add authentication, rate limits, request-size limits at the reverse proxy, malware scanning, secure transport, retention controls, and a documented deletion process.
- Do not infer or use protected personal characteristics for screening.
- Do not rank candidates automatically or use the score as a hiring decision.
- Make the method visible and let users correct extraction errors.
- Treat all resume content as unverified user-provided text.

The app currently extracts text only; it does not perform OCR on scanned PDF images.
