from langgraph.graph import StateGraph, END

from graph.state_schema import Evaluator_State

from graph.nodes import (
    input,
    test,
    human_feedback,
    eval,
    feedback,
    history,
)

from graph.constants import (
    INPUT,
    TEST,
    HUMAN_FEEDBACK,
    EVAL,
    FEEDBACK,
    HISTORY,
)

def should_continue(state: Evaluator_State):
    if len(state["question"]) > 5:
        return FEEDBACK
    return EVAL

builder = StateGraph(state_schema=Evaluator_State)
builder.add_node(INPUT,input)
builder.add_node(TEST,test)
builder.add_node(HUMAN_FEEDBACK,human_feedback)
builder.add_node(EVAL,eval)
builder.add_node(FEEDBACK,feedback)
builder.add_node(HISTORY,history)

builder.set_entry_point(INPUT)
builder.add_edge(INPUT,TEST)
builder.add_edge(TEST,HUMAN_FEEDBACK)
builder.add_edge(HUMAN_FEEDBACK,EVAL)
builder.add_conditional_edges(
    EVAL,
    should_continue,
    path_map = {
        TEST: TEST,
        FEEDBACK: FEEDBACK,
    }
)
builder.add_edge(FEEDBACK,HISTORY)
builder.add_edge(HISTORY,END)

graph = builder.compile()