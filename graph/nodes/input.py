from graph.state_schema import Evaluator_State

def input_node(state: Evaluator_State):
    subject_background = "A python developer"
    return {
        "subject_background": subject_background,
    }