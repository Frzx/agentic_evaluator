from typing import TypedDict,Annotated
import operator

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class Evaluator_State(TypedDict):
    subject_background: str
    topic: str
    messages: Annotated[list[BaseMessage], add_messages]
    scores: Annotated[list[float], operator.add]
    assessment: str