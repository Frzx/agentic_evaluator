from graph.state_schema import Evaluator_State

def feedback(state: Evaluator_State):
    assessment = "Need more work"
    return {
        "assessment": assessment
    }