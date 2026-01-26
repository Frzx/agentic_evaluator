from graph.state_schema import Evaluator_State
from core.logger import AppLogger

logger = AppLogger(__name__)

def history(state: Evaluator_State):
    logger.info("<SAVING HISTORY>")