import streamlit as st
from langchain_core.messages import HumanMessage,ToolMessage
import requests
import torch

from long_term_memory import agent
torch.classes.__path__ = []

old_request = requests.request

# Monkey patch requests to disable SSL verification
def patched_request(method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(method, url, **kwargs)

requests.request = patched_request


def abrir_chat(prompt):
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    messages = st.session_state.messages
    
    if prompt:
        messages.append(HumanMessage(content=prompt))
        st.spinner("Aguarde a resposta do modelo...")
        response = agent.invoke({"messages": messages})
        print(response)
        st.session_state.messages = response["messages"]
        for message in st.session_state.messages:
            if message.type != "tool":
                with st.chat_message(message.type):
                    st.write(message.content)

def meu_app():
    st.title("Chat com OpenAI")
    st.header("LuIA - O Assistente de IA",divider=True)
    st.markdown("### Converse com o luIA, seu assistente de IA personalizado.")
    prompt = st.chat_input("Digite a sua mensagem:")
    
    abrir_chat(prompt)
        
meu_app()