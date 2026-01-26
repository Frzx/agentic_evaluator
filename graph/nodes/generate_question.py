from graph.state_schema import Evaluator_State
from graph.chains.generate_question import chain
from core.logger import AppLogger

logger = AppLogger(__name__)

def generate_question(state: Evaluator_State):
    logger.info("<GENERATING QUESTION>")
    question = chain.invoke({
        "topic": state["topic"],
        "subject_background": state["subject_background"],
        "qna": state["qna"]
    })
    return {
        "qna": [question]
    }