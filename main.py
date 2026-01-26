import uuid

from dotenv import load_dotenv
from langgraph.graph.state import CompiledStateGraph    

from graph.evluator_graph import graph
from graph.constants import HITL, GENERATE_QUESTION, EVALUATE_ANSWER
from langchain_core.messages import HumanMessage, BaseMessage

from core.logger import AppLogger

load_dotenv()

logger = AppLogger(__name__)

class StreamPrinter:
    def __init__(self):
        self.last_msg_id = None
        self.last_node = None

    def consume(self, msg: BaseMessage, metadata: dict):

        node = metadata.get("langgraph_node","UNK")

        if self.last_node != node:
            print()
            self.last_node = node
        elif self.last_msg_id != msg.id:
            print()
            if node == GENERATE_QUESTION:
                print("[AI] : ", end="", flush=True)
            elif node == EVALUATE_ANSWER:
                print("[AI (evaluation)] : ", end="", flush=True)
            self.last_msg_id = msg.id
            
        if node in (GENERATE_QUESTION,EVALUATE_ANSWER) and msg.content:
            print(msg.content,end="",flush=True)

    def close(self):
        print('')


def run_graph(
    graph: CompiledStateGraph,
    thread: dict,
    input_state: dict|None = None,
):
    printer = StreamPrinter()
    for msg, metadata in graph.stream(
        input=input_state,
        config=thread,
        stream_mode="messages",
    ):
        # logger.debug(msg,metadata)
        printer.consume(msg,metadata)
    printer.close()

def handle_hitl(graph:CompiledStateGraph,thread:dict):

    user_answer = input("\n[YOU]: ")

    graph.update_state(
        thread, 
        {"qna": [HumanMessage(content=user_answer)]},
        as_node=HITL
    )
    logger.info("Updated user answer at HITL")


def main():
    print("=== Learning Evaluator Agent ===")
    thread = {"configurable": {"thread_id": str(uuid.uuid4())}}
    resume_path = r"C:\FARAZ\Documents\6. RESUME & so\AI, data scientist\format 5\resume_ahmad_faraz.pdf"
    topic = input("Enter the topic you want to learn: ")
    initial_state = {
        "qna": [],
        "subject_background": "Python Developer",
        "topic": topic,
        "evaluations": [],
        "feedback": None,
        "resume_filepath": resume_path
    }

    # First run # The graph will stop at before HITL NODE
    logger.info("Starting graph execution")
    run_graph(graph,thread,initial_state)
    
    snapshot = graph.get_state(thread)

    while snapshot.next and snapshot.next[0] == HITL:

        logger.info("Interrupted before HITL")

        # update the graph with user answer and print the generated question
        handle_hitl(graph,thread)
        # resume graph from hitl with either of the following paths
        # hitl - evaluate - generate
        # hitl - evaluate - feedback - history - end
        logger.info("resuming from HITL node")
        run_graph(graph,thread)
    
        snapshot = graph.get_state(thread)

    logger.info("Reached the end node")
    if snapshot.values["feedback"]:
        last = snapshot.values["feedback"].content
        print("\n[AI (feedback)]:", last)


if __name__ == "__main__":
    main()
