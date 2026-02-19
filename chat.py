import streamlit as st
from langchain_core.messages import HumanMessage
import requests

old_request = requests.request

# Monkey patch requests to disable SSL verification
def patched_request(method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(method, url, **kwargs)

requests.request = patched_request

from modelo_huggingface import model, messages

def abrir_chat(prompt,model,messages):
    if 'messages' in st.session_state:
        messages = st.session_state['messages']
    else:
        st.session_state['messages'] = messages
    if prompt:
        messages.append(HumanMessage(content=prompt))
        response = model.invoke(messages)
        messages.append(response)
    for message in messages:
        if message.type != "system":
            with st.chat_message(message.type):
                st.write(message.content)

def meu_app():
    st.title("Chat com OpenAI")
    st.header("LuIA - O Assistente de IA",divider=True)
    st.markdown("### Converse com o luIA, seu assistente de IA personalizado.")
    
    prompt = st.chat_input("Digite a sua mensagem:")
    
    abrir_chat(prompt,model,messages)
        
meu_app()