from graph.state_schema import Evaluator_State
from core.logging_config import get_dev_logger

logger = get_dev_logger(__name__)

def hitl(state: Evaluator_State):
    logger.info("<HITL>")
    