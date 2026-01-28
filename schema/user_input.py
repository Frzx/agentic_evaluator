from pydantic import BaseModel
from uuid import UUID

class BaseUserInput(BaseModel):
    thread_id: str
    user_id: str

class StartRequest(BaseUserInput):
    topic: str = "python basics"
    subject_background: str = "Python Developer"
    resume_filepath: str =  "./documents/resume.pdf"

class ResumeRequest(BaseUserInput):
    user_answer: str