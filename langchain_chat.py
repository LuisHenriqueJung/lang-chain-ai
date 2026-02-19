import streamlit as st
from langchain_core.messages import HumanMessage
from chat_chain import chain
import requests
import torch

torch.classes.__path__ = []

old_request = requests.request

# Monkey patch requests to disable SSL verification
def patched_request(method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(method, url, **kwargs)

requests.request = patched_request


def abrir_chat(prompt,chain):
    if 'messages' in st.session_state:
        messages = st.session_state['messages']
    else:
        messages = []
        st.session_state['messages'] = messages
    if prompt:

        messages.append(HumanMessage(content=prompt))
        st.spinner("Aguarde a resposta do modelo...")
        response = chain.invoke({"history": messages})
        messages.append(response)
        st.session_state['messages'] = messages
        
        for message in messages:
            if message.type != "system":
                with st.chat_message(message.type):
                    st.write(message.content)

def meu_app():
    st.title("Chat com OpenAI")
    st.header("LuIA - O Assistente de IA",divider=True)
    st.markdown("### Converse com o luIA, seu assistente de IA personalizado.")
    prompt = st.chat_input("Digite a sua mensagem:")
    
    abrir_chat(prompt, chain)
        
meu_app()