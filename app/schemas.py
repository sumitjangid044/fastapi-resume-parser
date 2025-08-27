from pydantic import BaseModel, Field
from typing import Optional, List

class CandidateOut(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    years_experience: Optional[float] = None
    target_role: str
    eligible: bool
    resume_filename: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    message: str = Field(default="Candidate processed")
    candidate: CandidateOut
    email_sent: bool = False
    dry_run: bool = True
