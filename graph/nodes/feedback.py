from graph.state_schema import Evaluator_State
from graph.chains.feedback import chain
from core.logging_config import get_dev_logger

logger = get_dev_logger(__name__)

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