from graph.state_schema import Evaluator_State

def test(state: Evaluator_State):
    # generate 1 question at a time
    q = "What is a Python generator?"
    state["questions"].append(q)
    return state