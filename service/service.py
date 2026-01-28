import json
from uuid import uuid4, UUID
from typing import AsyncGenerator,Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessageChunk
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from scalar_fastapi import get_scalar_api_reference

from graph.evluator_graph import graph
from core.logger import AppLogger
from schema.user_input import StartRequest, ResumeRequest

logger = AppLogger(__name__)

app = FastAPI(title="Evaluator Agent Service")


async def _handle_input(user_input: StartRequest|ResumeRequest) -> tuple[dict[str, Any], UUID]:
    """
    Parse user input and handle any required interrupt resumption.
    Returns kwargs for agent invocation and the run_id.
    """
    run_id = uuid4()
    thread_id = user_input.thread_id 
    user_id = user_input.user_id

    configurable = {"thread_id": thread_id, "user_id": user_id}


    config = RunnableConfig(
        configurable=configurable,
        run_id=run_id,
    )

    # Check for interrupts that need to be resumed
    state = await graph.aget_state(config=config)
    interrupted_tasks = [
        task for task in state.tasks if hasattr(task, "interrupts") and task.interrupts
    ]

    input: Command | dict[str, Any]
    if interrupted_tasks:
        # assume user input is response to resume agent execution from interrupt
        logger.info("INTERUPPTED AT HITL")
        input = Command(resume=user_input.user_answer)
    else:
        logger.info("STARTING INITIAL STATE")
        input =  {
        "qna": [],
        "subject_background": "",
        "topic": user_input.topic,
        "evaluations": [],
        "feedback": None,
        "resume_filepath": user_input.resume_filepath,
    }

    kwargs = {
        "input": input,
        "config": config,
    }

    return kwargs, run_id


async def message_generator(
    user_input: StartRequest|ResumeRequest
) -> AsyncGenerator[str, None]:
    
    kwargs, run_id = await _handle_input(user_input)

    try:
        async for stream_event in graph.astream(
            **kwargs,
            stream_mode=["updates", "messages"],
            subgraphs=True,
        ):
            if not isinstance(stream_event, tuple):
                continue

            _, stream_mode, event = stream_event

            # -------- HITL interrupt detection --------
            if stream_mode == "updates":
                for node in event:
                    if node == "__interrupt__":
                        yield f"data: {json.dumps({'type': 'hitl'})}\n\n"

            # -------- Token streaming --------
            if stream_mode == "messages":
                msg, _metadata = event
                if not isinstance(msg, AIMessageChunk):
                    continue
                if msg.content:
                    yield f"data: {json.dumps({'type': 'token', 'content': msg.content})}\n\n"

    except Exception as e:
        logger.error(f"Streaming error: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': 'Internal error'})}\n\n"

    finally:
        yield "data: [DONE]\n\n"


@app.post("/stream", response_class=StreamingResponse)
async def stream(user_input: StartRequest|ResumeRequest) -> StreamingResponse:
    """
    Stream an agent's response to a user input, including intermediate messages and tokens.

    Use thread_id to persist and continue a multi-turn conversation. run_id kwarg
    is also attached to all messages for recording feedback.

    """
    return StreamingResponse(
        message_generator(user_input),
        media_type="text/event-stream",
    )

@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url= app.openapi_url,
        title = "Scalar",
    )