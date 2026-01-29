from pydantic import BaseModel

class BaseUserInput(BaseModel):
    thread_id: str
    user_id: str

class StartRequest(BaseUserInput):
    topic: str = "python basics"
    resume_filepath: str =  "./documents/resume.pdf"

class ResumeRequest(BaseUserInput):
    user_answer: str