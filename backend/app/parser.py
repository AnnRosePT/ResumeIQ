from io import BytesIO
from pathlib import Path
from docx import Document
from pypdf import PdfReader


class ResumeParseError(ValueError):
    pass


def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    try:
        if suffix == ".txt":
            text = content.decode("utf-8-sig")
        elif suffix == ".pdf":
            reader = PdfReader(BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif suffix == ".docx":
            document = Document(BytesIO(content))
            paragraphs = [p.text for p in document.paragraphs]
            for table in document.tables:
                for row in table.rows:
                    paragraphs.append(" | ".join(cell.text for cell in row.cells))
            text = "\n".join(paragraphs)
        else:
            raise ResumeParseError("Unsupported file type. Upload PDF, DOCX, or TXT.")
    except ResumeParseError:
        raise
    except Exception as exc:
        raise ResumeParseError("Could not read this file. Check that it is a valid PDF, DOCX, or TXT.") from exc

    text = text.strip()
    if len(text) < 30:
        raise ResumeParseError(
            "Not enough readable text was found. Try a text-based PDF or DOCX; scanned PDFs need OCR."
        )
    return text[:100_000]
