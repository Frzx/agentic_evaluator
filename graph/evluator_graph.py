from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state_schema import Evaluator_State

from graph.nodes import (
    input_node,
    generate_question,
    hitl,
    evaluate_answer,
    feedback,
    history,
)

from graph.constants import (
    INPUT_NODE,
    GENERATE_QUESTION,
    HITL,
    EVALUATE_ANSWER,
    FEEDBACK,
    HISTORY,
)

def should_continue(state: Evaluator_State):
    # print(len(state["messages"]))
    if len(state["qna"]) > 2:
        return FEEDBACK
    return GENERATE_QUESTION

builder = StateGraph(state_schema=Evaluator_State)
builder.add_node(INPUT_NODE,input_node)
builder.add_node(GENERATE_QUESTION,generate_question)
builder.add_node(HITL,hitl)
builder.add_node(EVALUATE_ANSWER,evaluate_answer)
builder.add_node(FEEDBACK,feedback)
builder.add_node(HISTORY,history)

builder.set_entry_point(INPUT_NODE)
builder.add_edge(INPUT_NODE,GENERATE_QUESTION)
builder.add_edge(GENERATE_QUESTION,HITL)
builder.add_edge(HITL,EVALUATE_ANSWER)
builder.add_conditional_edges(
    EVALUATE_ANSWER,
    should_continue,
    path_map = {
        GENERATE_QUESTION: GENERATE_QUESTION,
        FEEDBACK: FEEDBACK,
    }
)
builder.add_edge(FEEDBACK,HISTORY)
builder.add_edge(HISTORY,END)


memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory,
    interrupt_before=[HITL]
)