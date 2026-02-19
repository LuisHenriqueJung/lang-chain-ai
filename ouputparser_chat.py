from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser


modelo = ChatOpenAI()

template_chat = ChatPromptTemplate([
    SystemMessage("Responda o usuário sempre em {idioma} independente da língua que ele usar na pergunta"),
    SystemMessage("Gere uma lista com 10 produtos de {produto}, com quantidades em estoque e preços. A resposta deve ser formatada como um JSON válido seguindo as instruções de formatação."),
], partial_variables={"idioma": "ingles", "produto": "informática"})

texto_usuario = input("Digite o tipo de produto: ")
template_chat.partial_variables
mensagem_usuario = HumanMessage(texto_usuario)
template_chat.append(mensagem_usuario)

prompt = template_chat.invoke({})
resposta = modelo.invoke(prompt)
parser = StrOutputParser()
resposta = parser.invoke(resposta)

print(resposta)
