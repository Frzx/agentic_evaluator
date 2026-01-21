from graph.state_schema import Evaluator_State

def feedback(state: Evaluator_State):
    state["history"].append(state["evaluation"])
    return state