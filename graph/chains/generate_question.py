from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


system_prompt = """
You are an evaluator.
Your task is to generate a question for a subject based on the user's background and the provided topic.
Ask one question at a time. Adjust the difficulty based on previous answers to the questions, if any.
"""

prompt = ChatPromptTemplate.from_messages([
    ('system',system_prompt),
    ("human", "Topic: {topic}\nSubject background: {subject_background}"),
    MessagesPlaceholder(variable_name="qna")
])

llm = ChatOpenAI()

chain = prompt | llm