from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()

system_prompt = """
You are an evaluator.

Your task is to objectively evaluate ONLY the user's latest answer to the latest question.

Evaluation rules:
- Assess factual correctness, completeness, and relevance.
- Do NOT provide hints, follow-up questions, or teaching.
- Provide a concise, neutral evaluation.
"""

prompt = ChatPromptTemplate.from_messages([
    ('system',system_prompt),
    ("human", "Topic: {topic}\nSubject background: {subject_background}"),
    MessagesPlaceholder(variable_name="qna")
])

llm = ChatOpenAI(temperature=0.3)

chain = prompt | llm