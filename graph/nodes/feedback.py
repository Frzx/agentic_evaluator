from graph.state_schema import Evaluator_State
from graph.chains.feedback import chain

def feedback(state: Evaluator_State):
    print("---GENERATING FEEDBACK---")
    feedback = chain.invoke({
        "qna": state["qna"],
        "topic": state["topic"],
        "subject_background": state["subject_background"]
    })
    return {
        "feedback": feedback
    }