from graph.state_schema import Evaluator_State
from graph.chains.feedback import chain
from core.logger import AppLogger

logger = AppLogger(__name__)

def feedback(state: Evaluator_State):
    logger.info("<GENERATING FEEDBACK>")
    feedback = chain.invoke({
        "qna": state["qna"],
        "topic": state["topic"],
        "subject_background": state["subject_background"]
    })
    return {
        "feedback": feedback
    }