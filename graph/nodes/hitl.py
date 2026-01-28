from langgraph.types import interrupt
from langchain_core.messages import HumanMessage

from graph.state_schema import Evaluator_State
from core.logger import AppLogger

logger = AppLogger(__name__)

def hitl(state: Evaluator_State):
    logger.info("<HITL>")
    generated_question = state["qna"][-1].content
    user_answer = interrupt(
        # This value will be sent to the client
        # as part of the interrupt information.
        f"{generated_question}"
    )
    return {
        "qna": [HumanMessage(content=user_answer)]
    }
    
    