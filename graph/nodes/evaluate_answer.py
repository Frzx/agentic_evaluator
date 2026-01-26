from graph.state_schema import Evaluator_State
from graph.chains.evaluate_answers import chain
from core.logger import AppLogger

logger = AppLogger(__name__)


def evaluate_answer(state: Evaluator_State):
    logger.info("<EVALUATING ANSWER>")
    evaluation = chain.invoke({
        "topic": state["topic"],
        "subject_background": state['subject_background'],
        "qna": state["qna"][-2:]
    })
    return {"evaluations": [evaluation]}
