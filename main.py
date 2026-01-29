import asyncio
import uuid
import httpx
import json

from dotenv import load_dotenv

from core.logger import AppLogger

load_dotenv()

logger = AppLogger(__name__)


stream_url = "http://localhost:8000/stream"
async def reply(payload):
    async with httpx.AsyncClient() as client:
        async with client.stream("POST",stream_url,json=payload,timeout=None) as response:
            async for line in response.aiter_lines():

                if not line.startswith("data: "):
                    continue

                data_content = line.replace("data: ","")

                if data_content == "[DONE]":
                    break

                event = json.loads(data_content)
                if event["type"] == "token":
                    print(event["content"],end="",flush=True)
                elif event["type"] == "hitl":
                    break



async def main():
    print("=== Learning Evaluator Agent ===")
    thread_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    resume_path = "./documents/resume.pdf"
    topic = input("Enter the topic you want to learn: ")
    payload = {
        "thread_id": thread_id,
        "user_id": user_id,
        "topic": topic,
        "resume_filepath": resume_path
    }
    while True:
        print("[AI]: ",end="")
        await reply(payload)
        print("\n")
        user_input = input("[You]: ")
        print("\n")
        payload = {
            "thread_id": thread_id,
            "user_id": user_id,
            "user_answer": user_input,
        }



if __name__ == "__main__":
    # start t: uv run uvicorn service.service:app --reload
    asyncio.run(main())
