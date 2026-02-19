

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory


chats = {}

def get_session_history(session_id):
    if session_id not in chats:
        chats[session_id] = InMemoryChatMessageHistory()
    return chats[session_id]
        
chat_template = ChatPromptTemplate(
    [
        ("system", "Responda o usuário com respostas diretas e o mais curtas possíveis, mas sempre respondendo a dúvida dele. As dúvidas são referentes a programação em {tema}. Qualquer outra dúvida que não seja desse tema apenas responda: não sou especialista no tema"),
        ("placeholder", "{history}"),
        ("user", "{message}")
    ], partial_variables={"tema": "Python"}
)

model = ChatOpenAI()


chain = chat_template | model   

with_memory_chain = RunnableWithMessageHistory(chain,
                                               get_session_history=get_session_history, 
                                               input_messages_key="message",
                                               history_messages_key="history")