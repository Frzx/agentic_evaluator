from graph.state_schema import Evaluator_State
from core.logger import AppLogger

logger = AppLogger(__name__)

def input_node(state: Evaluator_State):
    logger.info("<INPUT NODE>")
    subject_background = "A python developer"
    return {
        "subject_background": subject_background,
    }