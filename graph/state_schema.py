from typing import TypedDict

class Evaluator_State(TypedDict):
    subject_background: str
    topic: str
    questions: list[str]
    user_answers: list[str]
    score: list[str]
    assessment: str