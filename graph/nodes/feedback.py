from graph.state_schema import Evaluator_State

def feedback(state: Evaluator_State):
    print("---GENERATING FEEDBACK---")
    assessment = "Need more work"
    return {
        "assessment": assessment
    }