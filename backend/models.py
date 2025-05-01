from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    role: str

class ChallengeCreate(BaseModel):
    title: str
    description: str

class Challenge(BaseModel):
    id: str
    title: str
    description: str
    posted_by: str
    created_at: datetime

class SubmissionCreate(BaseModel):
    code: str
    challenge_id: str

class Submission(BaseModel):
    id: str
    code: str
    student_id: str
    challenge_id: str
    feedback: Optional[str]
    score: Optional[float]
    created_at: datetime

class PortfolioResponse(BaseModel):
    submissions: List[Submission]
