import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk, ToolMessage
import requests
import torch
import json
import os

from long_term_memory import agent
torch.classes.__path__ = []

old_request = requests.request

# Monkey patch requests to disable SSL verification
def patched_request(method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(method, url, **kwargs)

requests.request = patched_request

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            # Convert back to message objects
            messages = []
            for msg in data:
                if msg['type'] == 'human':
                    messages.append(HumanMessage(content=msg['content']))
                elif msg['type'] == 'ai':
                    messages.append(AIMessage(content=msg['content']))
                # Add other types if needed
            return messages
    return []

def save_history(messages):
    data = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            data.append({'type': 'human', 'content': msg.content})
        elif isinstance(msg, AIMessage):
            data.append({'type': 'ai', 'content': msg.content})
        # Add other types if needed
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f)


def abrir_chat(prompt):
    if 'messages' not in st.session_state:
        st.session_state.messages = load_history()
    
    messages = st.session_state.messages
    
    if prompt:
        messages.append(HumanMessage(content=prompt))
        
        # Display user message
        with st.chat_message("human"):
            st.write(prompt)
        
        # Prepare for AI response
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            input_message = {"messages": messages}
            for stream_mode, data in agent.stream(
                input_message,
                stream_mode=["messages", "updates"],  
            ):
                if stream_mode == "messages":
                    token, metadata = data
                    if isinstance(token, AIMessageChunk):
                        if token.content:
                            full_response += token.content
                            placeholder.write(full_response)
            
            # Append the full AI message to session state
            messages.append(AIMessage(content=full_response))
            st.session_state.messages = messages
            save_history(messages)

def meu_app():
    st.title("Chat com OpenAI")
    st.header("LuIA - O Assistente de IA", divider=True)
    st.markdown("### Converse com o luIA, seu assistente de IA personalizado.")
    
    # Load and display existing history
    if 'messages' not in st.session_state:
        st.session_state.messages = load_history()
    
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("human"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)
    
    prompt = st.chat_input("Digite a sua mensagem:")
    
    abrir_chat(prompt)
        
meu_app()