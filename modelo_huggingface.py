import os

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

messages = [
    SystemMessage(content="You are a helpful assistant.No máximo 140 caracteres.")
    ]

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
)

model = ChatHuggingFace(llm=llm)

def get_model(llmId):
    llm = HuggingFaceEndpoint(
        repo_id=llmId,
    )
    return ChatHuggingFace(llm=llm)
if __name__ == "__main__":
    prompt = input("Digite a sua mensagem: ")  # Test prompt instead of input
    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages)