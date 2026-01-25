from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()

system_prompt = """
You are evaluator of an person answering question based on the topic selected and the professional background
Evaluate the lastest answer to the latest question.
"""

prompt = ChatPromptTemplate.from_messages([
    ('system',system_prompt),
    ("human", "Topic: {topic}\nSubject background: {subject_background}"),
    MessagesPlaceholder(variable_name="qna")
])

llm = ChatOpenAI(temperature=0.3)

chain = prompt | llm