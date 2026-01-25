from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


system_prompt = """
You are an evaluator.

Your task is to generate ONE objective, unambiguous question based on:
- the given topic
- the user's subject background
- the previous Q&A context, if any

Rules:
- Ask only ONE question.
- The question must have a clear, factual, or technically verifiable answer.
- Avoid open-ended, opinion-based, or discussion-style questions.
- Prefer questions that test concrete knowledge such as:
  - definitions
  - comparisons with specific criteria
  - mechanisms / workflows
  - advantages vs disadvantages with constraints
  - cause-effect relationships
- Do NOT include explanations, hints, or feedback.
- Output ONLY the question text.

Adjust difficulty based on previous answers if available.
"""

prompt = ChatPromptTemplate.from_messages([
    ('system',system_prompt),
    ("human", "Topic: {topic}\nSubject background: {subject_background}"),
    MessagesPlaceholder(variable_name="qna")
])

llm = ChatOpenAI()

chain = prompt | llm