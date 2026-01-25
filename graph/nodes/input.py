from graph.state_schema import Evaluator_State
from core.logging_config import get_dev_logger

logger = get_dev_logger(__name__)

def input_node(state: Evaluator_State):
    logger.info("<INPUT NODE>")
    subject_background = "A python developer"
    return {
        "subject_background": subject_background,
    }