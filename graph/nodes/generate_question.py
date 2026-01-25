from graph.state_schema import Evaluator_State

from graph.chains.generate_question import chain

def generate_question(state: Evaluator_State):
    print("---GENERATING QUESTION---")
    question = chain.invoke({
        "topic": state["topic"],
        "subject_background": state["subject_background"],
        "qna": state["qna"]
    })
    return {
        "qna": [question]
    }