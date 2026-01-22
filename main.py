from dotenv import load_dotenv
from graph.evluator_graph import graph
from graph.constants import HITL
from langchain_core.messages import HumanMessage

load_dotenv()

THREAD = {"configurable": {"thread_id": "1"}}

def main():
    print("=== Learning Evaluator Agent ===")

    topic = input("Enter the topic you want to learn: ")

    initial_state = {
        "messages": [],
        "subject_background": "",
        "topic": topic,
        "scores": [],
        "assessment": ""
    }

    # First run # The graph will stop at before HITL NODE
    for _ in graph.stream(initial_state, THREAD, stream_mode="values"):
        pass

    snapshot = graph.get_state(THREAD)
    next_node = snapshot.next[0]
    print("NEXT NODE: ", next_node)

    while next_node == HITL:

        user_answer = input("\nYour answer: ")

        graph.update_state(
            THREAD,
            {"messages": [HumanMessage(content=user_answer)]},
            as_node=HITL
        )
    
        # Resume after HITL # TWO PATHS: IN FIRST PATH GRAPH WILL REACH END NODE, IN SECOND PATH GRAPH WILL REACH HITL NODE
        for _ in graph.stream(None, THREAD, stream_mode="values"):
            pass

        snapshot = graph.get_state(THREAD)
        
        next_node = snapshot.next[0] if snapshot.next else None
        print("NEXT NODE: ", next_node)

if __name__ == "__main__":
    main()
