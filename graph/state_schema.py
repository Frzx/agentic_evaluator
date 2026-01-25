from typing import TypedDict,Annotated

from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph.message import add_messages

class Evaluator_State(TypedDict):
    subject_background: str
    topic: str
    qna: Annotated[list[BaseMessage],add_messages]
    evaluations: Annotated[list[AIMessage],add_messages]
    assessment: str