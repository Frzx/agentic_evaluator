from graph.state_schema import Evaluator_State

def eval(state: Evaluator_State):
    state["evaluation"] = "Partial understanding"
    return state
