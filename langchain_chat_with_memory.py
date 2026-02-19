from chat_chain_with_memory import with_memory_chain,chats
import requests
import streamlit as st

old_request = requests.request

# Monkey patch requests to disable SSL verification
def patched_request(method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(method, url, **kwargs)

requests.request = patched_request


def abrir_chat(prompt,with_memory_chain,chats):
    tema = st.selectbox("Escolha o tema da conversa:", options=["Programação em Python","Matemática","História"])
    print(tema)
    config = {"configurable": {"session_id": tema}} 
    if prompt:
        with_memory_chain.invoke({"message": prompt,"tema": tema},config=config)
    if tema in chats:
        for message in chats[tema].messages:
            if message.type != "system":
                with st.chat_message(message.type):
                    st.write(message.content)

def meu_app():
    st.title("Chat com OpenAI")
    st.header("LuIA - O Assistente de IA",divider=True)
    st.markdown("### Converse com o luIA, seu assistente de IA personalizado.")
    prompt = st.chat_input("Digite a sua mensagem:")
    
    abrir_chat(prompt, with_memory_chain,chats)
        
meu_app()