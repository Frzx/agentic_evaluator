import logging

from dotenv import load_dotenv
from graph.evluator_graph import graph
from graph.constants import HITL, EVALUATE_ANSWER
from langchain_core.messages import HumanMessage,AIMessage

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename="app.log",mode='w',encoding="utf-8")
log_formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)

load_dotenv()

THREAD = {"configurable": {"thread_id": "1"}}

def main():
    print("=== Learning Evaluator Agent ===")

    # topic = input("Enter the topic you want to learn: ")

    initial_state = {
        "qna": [],
        "subject_background": "Python Developer",
        "topic": "Deep learning",
        "evaluations":[],
        "assessment": "",
    }

    # First run # The graph will stop at before HITL NODE
    logger.info("Starting graph execution")
    for state in graph.stream(initial_state, THREAD, stream_mode="values"):
        logger.debug(state)
    logger.info("Interrupted before HITL")

    snapshot = graph.get_state(THREAD)
    next_node = snapshot.next[0]

    while next_node == HITL:
        snapshot = graph.get_state(THREAD)
        # ---- Print AI response ----
        if snapshot.values["qna"]:
            last = snapshot.values["qna"][-1]
            if isinstance(last, AIMessage):
                print("\nAI:", last.content)

        user_answer = input("\nYour answer: ")

        graph.update_state(
            THREAD,
            {"qna": [HumanMessage(content=user_answer)]},
            as_node=HITL
        )
    

        # Resume after HITL # TWO PATHS: IN FIRST PATH GRAPH WILL REACH END NODE, IN SECOND PATH GRAPH WILL REACH HITL NODE
        n_evaluations = len(snapshot.values["evaluations"])
        for state in graph.stream(None, THREAD, stream_mode="values"):
            logger.debug(state)
            if len(state["evaluations"]) > n_evaluations:
                last = state["evaluations"][-1]
                n_evaluations = len(state["evaluations"])
                print("\nAI Evaluation: ", last.content)


        logger.info("Interrupted before HITL")

        # print the evaluation
        # snapshot = graph.get_state(THREAD)
        # if snapshot.values["evaluations"]:
        #     last = snapshot.values["evaluations"][-1]
        #     print("\nAI: ", last.content)


        snapshot = graph.get_state(THREAD)
        next_node = snapshot.next[0] if snapshot.next else None

    snapshot = graph.get_state(THREAD)
    if snapshot.values["assessment"]:
        last = snapshot.values["assessment"]
        print("\nAI:",last)

if __name__ == "__main__":
    main()
