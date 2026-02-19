import streamlit as st
from langchain_core.messages import HumanMessage
import requests
import torch

torch.classes.__path__ = []

old_request = requests.request

# Monkey patch requests to disable SSL verification
def patched_request(method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(method, url, **kwargs)

requests.request = patched_request

from modelo_huggingface import get_model, model, messages

def abrir_chat(prompt,modelId,messages):
    if 'messages' in st.session_state:
        messages = st.session_state['messages']
    else:
        st.session_state['messages'] = messages
    if prompt:
        messages.append(HumanMessage(content=prompt))
        st.spinner("Aguarde a resposta do modelo...")
        response = get_model(modelId).invoke(messages)
        print(response)
        if '</think>' in response.content:
            messages.append(HumanMessage(content=response.content.split('</think>')[1]))
        else:
            messages.append(response)
    for message in messages:
        if message.type != "system":
            with st.chat_message(message.type):
                st.write(message.content)

def meu_app():
    st.title("Chat com OpenAI")
    st.header("LuIA - O Assistente de IA",divider=True)
    st.markdown("### Converse com o luIA, seu assistente de IA personalizado.")
    modelId = st.selectbox("Escolha o modelo de linguagem:", options=["deepseek-ai/DeepSeek-R1-Distill-Qwen-32B","meta-llama/Llama-3.1-8B-Instruct","openai/gpt-oss-20b"], key="modelId")
    prompt = st.chat_input("Digite a sua mensagem:")
    
    abrir_chat(prompt,modelId,messages)
        
meu_app()