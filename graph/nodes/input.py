from graph.state_schema import Evaluator_State

def input_node(state: Evaluator_State):
    print("---INPUT NODE----")
    subject_background = "A python developer"
    return {
        "subject_background": subject_background,
    }