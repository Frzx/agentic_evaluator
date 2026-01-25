import logging

from dotenv import load_dotenv
from graph.evluator_graph import graph
from graph.constants import HITL
from langchain_core.messages import HumanMessage,AIMessage

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename="app.log",mode='w',encoding="utf-8")
log_formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
file_handler.setFormatter(log_formatter)

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
    for event in graph.stream(initial_state, THREAD, stream_mode="values"):
        logger.debug(event)
    logger.info("Reached HITL")

    snapshot = graph.get_state(THREAD)
    next_node = snapshot.next[0]

    while next_node == HITL:
        state = graph.get_state(THREAD)
        # ---- Print AI response ----
        if state.values["qna"]:
            last = state.values["qna"][-1]
            if isinstance(last, AIMessage):
                print("\nAI:", last.content)

        user_answer = input("\nYour answer: ")

        graph.update_state(
            THREAD,
            {"qna": [HumanMessage(content=user_answer)]},
            as_node=HITL
        )
    
        # Resume after HITL # TWO PATHS: IN FIRST PATH GRAPH WILL REACH END NODE, IN SECOND PATH GRAPH WILL REACH HITL NODE
        for _ in graph.stream(None, THREAD, stream_mode="values"):
            pass

        snapshot = graph.get_state(THREAD)
        
        next_node = snapshot.next[0] if snapshot.next else None

    state = graph.get_state(THREAD)
    if state.values["assessment"]:
        last = state.values["assessment"]
        print("\nAI:",last)

if __name__ == "__main__":
    main()
