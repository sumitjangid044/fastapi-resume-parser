import re
from typing import Dict
from io import BytesIO
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document
import logging
import uuid

logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+\d{1,3}[\s-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s-]?\d{3,4}[\s-]?\d{3,4}")
YEARS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:\+\s*)?(?:years?|yrs?)", re.IGNORECASE)

DEFAULT_SKILLS = [
    "java", "spring", "spring boot", "hibernate",
    "python", "fastapi", "django", "flask",
    "javascript", "typescript", "react", "node", "node.js", "express",
    "html", "css", "tailwind", "redux", "next.js",
    "sql", "mysql", "postgresql", "sqlite", "mongodb",
    "docker", "kubernetes", "k8s", "aws", "gcp", "azure",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "android", "kotlin", "swift", "react native", "flutter"
]

def _text_from_pdf(file_bytes: bytes) -> str:
    try:
        return pdf_extract_text(BytesIO(file_bytes)) or ""
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return ""

def _text_from_docx(file_bytes: bytes) -> str:
    try:
        doc = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        logger.error(f"DOCX extraction failed: {e}")
        return ""

def extract_text(filename: str, file_bytes: bytes) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        text = _text_from_pdf(file_bytes)
        if text.strip():
            return text

    if name.endswith(".docx"):
        text = _text_from_docx(file_bytes)
        if text.strip():
            return text

    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def parse_resume(filename: str, file_bytes: bytes) -> Dict:
    if len(file_bytes) < 500:
        raise ValueError("Uploaded file is too small or empty. Please upload a valid resume.")

    text = extract_text(filename, file_bytes).strip()
    if not text:
        raise ValueError("Could not extract text from resume. Please upload a valid PDF or DOCX.")

    lower_text = text.lower()
    email = EMAIL_RE.search(text)
    phone = PHONE_RE.search(text)

    candidates = [float(m.group(1)) for m in YEARS_RE.finditer(lower_text)]
    years = max(candidates) if candidates else None

    skills_found = [sk for sk in DEFAULT_SKILLS if sk in lower_text]

    name = None
    for line in text.splitlines():
        s = line.strip()
        if len(s.split()) >= 2 and any(c.isalpha() for c in s):
            name = s[:120]
            break

    eligible = True
    if years is not None and years < 0:
        eligible = False

    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "skills": skills_found,
        "years_experience": years,
        "eligible": eligible,
        "raw_text": text
    }
