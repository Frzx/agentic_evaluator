
from dotenv import load_dotenv

from graph.evluator_graph import graph
from graph.constants import HITL

load_dotenv()

THREAD = {"configurable": {"thread_id": "1"}}


def main():

    print("=== Learning Evaluator Agent ===")

    topic = input("Enter the topic you want to learn: ")


    initial_state = {
        "subject_background": "",
        "topic": topic,
        "questions": [],
        "user_answers": [],
        "score": "",
        "assessment": "",
        "history": []
    }

    # ---- First run until human interrupt ----
    for event in graph.stream(initial_state, THREAD, stream_mode="values"):
        print(event)

    print("\n--- Graph Paused At ---")
    print(graph.get_state(THREAD).next)


    # ---- Human provides answer ----
    user_input = input("\nYour answer: ")

    graph.update_state(
        THREAD,
        {"user_answers": [user_input]},
        as_node=HITL
    )

    print("\n--- State After Update ---")

    # ---- Resume execution ----
    for event in graph.stream(None, THREAD, stream_mode="values"):
        print(event)


if __name__ == "__main__":
    main()
