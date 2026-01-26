import uuid
import gradio as gr
from dotenv import load_dotenv
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage, AIMessageChunk

from graph.evluator_graph import graph
from graph.constants import HITL, GENERATE_QUESTION, EVALUATE_ANSWER
from core.logger import AppLogger

load_dotenv()
logger = AppLogger(__name__)

# =========================
# LangGraph Streaming (REFINED)
# =========================
def stream_graph(
    graph: CompiledStateGraph,
    thread: dict,
    input_state: dict | None = None,
):
    """
    Streams messages from the graph. 
    Handles multiple nodes (Evaluation -> Question) in one stream.
    """
    buffers = {} 
    node_order = [] # Tracks which nodes have sent data

    for msg, metadata in graph.stream(
        input=input_state,
        config=thread,
        stream_mode="messages",
    ):
        node = metadata.get("langgraph_node")
        
        # Only process nodes that generate UI content
        if node not in (GENERATE_QUESTION, EVALUATE_ANSWER):
            continue

        if not isinstance(msg, AIMessageChunk) or not msg.content:
            continue

        if node not in buffers:
            buffers[node] = ""
            node_order.append(node)

        buffers[node] += msg.content

        # Build the output string in the order nodes executed
        full_response = []
        for n in node_order:
            prefix = "### Evaluation\n" if n == EVALUATE_ANSWER else "### Next Question\n"
            full_response.append(f"{prefix}{buffers[n]}")

        yield "\n\n---\n\n".join(full_response)


# =========================
# Gradio Chat Handler
# =========================
def chat_fn(user_input, history):
    # Retrieve or initialize session state
    if not hasattr(chat_fn, "state"):
        chat_fn.state = {
            "thread": {"configurable": {"thread_id": str(uuid.uuid4())}},
            "initialized": False,
            "resume_path": "path_to_resume.pdf", 
        }
    
    state = chat_fn.state

    # ---------- Case 1: Start (Topic Injection) ----------
    if not state["initialized"]:
        state["initialized"] = True
        initial_state = {
            "qna": [],
            "subject_background": "Python Developer",
            "topic": user_input,
            "evaluations": [],
            "feedback": None,
            "resume_filepath": state["resume_path"],
        }
        
        # Stream the very first question
        last_chunk = ""
        for text in stream_graph(graph, state["thread"], initial_state):
            last_chunk = text
            yield text
        return

    # ---------- Case 2: Human-in-the-loop (Answer) ----------
    # We update the state with the user's answer
    graph.update_state(
        state["thread"],
        {"qna": [HumanMessage(content=user_input)]},
        as_node=HITL,
    )

    # Stream both Evaluation and the next Question
    last_output = ""
    for text in stream_graph(graph, state["thread"]):
        last_output = text
        yield text

    # ---------- Case 3: Check for Final Feedback ----------
    snapshot = graph.get_state(state["thread"])
    if snapshot.values.get("feedback"):
        final_fb = snapshot.values["feedback"]
        # If feedback is a Message object, get content, else use string
        fb_text = getattr(final_fb, 'content', str(final_fb))
        yield f"{last_output}\n\n---\n\n### Final Feedback\n{fb_text}"


# =========================
# App Launch
# =========================
def launch():
    # It's better to define the state here or use gr.State()
    # But to keep your logic working:
    chat_fn.state = {
        "thread": {"configurable": {"thread_id": str(uuid.uuid4())}},
        "initialized": False,
        "resume_path": r"C:\FARAZ\Documents\6. RESUME & so\AI, data scientist\format 5\resume_ahmad_faraz.pdf",
    }

    # Removed 'theme' to avoid the TypeError
    demo = gr.ChatInterface(
        fn=chat_fn,
        title="AI Interviewer & Tutor",
        description="I will evaluate your answers and guide you through the topic.",
    )
    demo.launch()

if __name__ == "__main__":
    launch()