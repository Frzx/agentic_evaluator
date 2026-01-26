import fitz

from graph.state_schema import Evaluator_State
from core.logger import AppLogger

logger = AppLogger(__name__)

def extract_pdf_text(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)


def input_node(state: Evaluator_State):
    logger.info("<INPUT NODE>")
    subject_background = extract_pdf_text(state["resume_filepath"])
    return {
        "subject_background": subject_background,
    }