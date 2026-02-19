from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

messages = [
    SystemMessage(content="You are a helpful assistant.No máximo 140 caracteres.")
    ]

model = ChatOpenAI()
if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages, max_tokens=140, temperature=0.7, stop=["\n"])
    print(response.content)
    print(response.usage_metadata)