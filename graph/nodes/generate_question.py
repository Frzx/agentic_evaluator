from graph.state_schema import Evaluator_State

from langchain_core.messages import AIMessage

def generate_question(state: Evaluator_State):
    print("---GENERATING QUESTION---")
    question = "What is an agent"
    return {
        "messages": [AIMessage(content=question)]
    }