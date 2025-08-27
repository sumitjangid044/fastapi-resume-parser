# Hiring Backend — Step 1 (FastAPI)

Covers:
- Resume upload (PDF/DOCX)
- Resume parsing → email/phone/skills/experience
- Role eligibility check (Java/Python/Fullstack/Frontend/AI-ML/App Dev/Data Analyst)
- Email trigger (DRY RUN by default — prints to console)
- Persistent DB (SQLite default)

## How to run (Step 1)

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# start the API
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

### Test the flow
Use `POST /candidates/upload` with form-data:
- `target_role`: one of
  `java_developer`, `python_developer`, `full_stack_developer`, `frontend_developer`, `ai_ml_engineer`, `app_developer`, `data_analyst`
- `resume`: upload a PDF or DOCX

The API will:
- Parse email/phone/skills/years
- Match against role rules
- Save candidate to DB
- If eligible, “send” an email (printed to console unless you set SMTP)

### (optional) real emails
Edit `.env` with your SMTP (e.g., Gmail app password) and set `DRY_RUN_EMAILS=false`.
