from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import streamlit as st


chat_template = ChatPromptTemplate(
    [
        SystemMessage("Responda o usuário com respostas diretas e o mais curtas possíveis, mas sempre respondendo a dúvida dele. As dúvidas são referentes a programação em {tema}. Qualquer outra dúvida que não seja desse tema apenas responda: não sou especialista no tema"),
        MessagesPlaceholder("history")
    ], partial_variables={"tema": "Python"}
)

model = ChatOpenAI()

chain = chat_template | model   