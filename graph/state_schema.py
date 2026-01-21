from typing import TypedDict


class Evaluator_State(TypedDict):
    subject_background: str
    topic: str
    question: list[str]
    answer: list[str]
    score: list[str]
    assessment: str