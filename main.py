import uuid

from dotenv import load_dotenv
from langgraph.graph.state import CompiledStateGraph

from graph.evluator_graph import graph
from graph.constants import HITL
from langchain_core.messages import HumanMessage, AIMessage

from core.logging_config import get_dev_logger

load_dotenv()

logger = get_dev_logger(__name__)


def run_graph(
    graph: CompiledStateGraph,
    thread: dict,
    input_state: dict = None,
):
    for state in graph.stream(input=input_state, config=thread, stream_mode="values"):
        logger.debug(state)

def handle_hitl(graph:CompiledStateGraph,thread:dict):
    snapshot = graph.get_state(thread)
    # ---- Print Question ----
    if snapshot.values["qna"]:
        last = snapshot.values["qna"][-1]
        if isinstance(last, AIMessage):
            print("\nAI:", last.content)

    user_answer = input("\nYour answer: ")

    graph.update_state(
        thread, {"qna": [HumanMessage(content=user_answer)]}, as_node=HITL
    )
    logger.info("Updated user answer at HITL")


def main():
    print("=== Learning Evaluator Agent ===")
    thread = {"configurable": {"thread_id": str(uuid.uuid4())}}
    topic = input("Enter the topic you want to learn: ")
    initial_state = {
        "qna": [],
        "subject_background": "Python Developer",
        "topic": topic,
        "evaluations": [],
        "feedback": None,
    }

    # First run # The graph will stop at before HITL NODE
    logger.info("Starting graph execution")
    run_graph(graph,thread,initial_state)
    

    snapshot = graph.get_state(thread)
    eval_count = len(snapshot.values["evaluations"])

    while snapshot.next and snapshot.next[0] == HITL:

        logger.info("Interrupted before HITL")

        # update the graph with user answer and print the generated question
        handle_hitl(graph,thread)
        # resume graph from hitl with either of the following paths
        # hitl - evaluate - generate
        # hitl - evaluate - feedback - history - end
        logger.info("resuming from HITL node")
        run_graph(graph,thread)
    
        # print the evaluation
        snapshot = graph.get_state(thread)
        if len(snapshot.values["evaluations"]) > eval_count:
            last = snapshot.values["evaluations"][-1]
            eval_count = len(snapshot.values["evaluations"])
            print("\nAI Evaluation: ", last.content)

        snapshot = graph.get_state(thread)

    logger.info("Reach the end node")
    if snapshot.values["feedback"]:
        last = snapshot.values["feedback"].content
        print("\nAI:", last)


if __name__ == "__main__":
    main()
