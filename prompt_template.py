from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

modelo = OpenAI()

# template_prompt = PromptTemplate.from_template("""Responda ao usuário em no máximo {tamanho} caracteres, responda em {idioma}, independente da língua que o usuário fizer a pergunta.
# Pergunta do usuário: {mensagem}
# """, partial_variables={"tamanho": 140, "idioma": "espanhol"})

template_forma = PromptTemplate.from_template("Responda o usuário de forma educada, porém informal, como se fosse um amigo falando com ele")
template_tamanho = PromptTemplate.from_template("A sua resposta deve ter sempre no máximo {tamanho} caracteres.", partial_variables={"tamanho": 140})
template_idioma = PromptTemplate.from_template("Responda em {idioma}, independente da língua que o usuário fizer a pergunta.", partial_variables={"idioma": "espanhol"})
template_mensagem = PromptTemplate.from_template("Mensagem do usuário: {mensagem}")
template_final = (template_forma + template_tamanho + template_idioma + template_mensagem)

prompt = template_final.invoke({"mensagem": "Python vale a pena aprender para quem não sabe nada?"})
print(prompt)

resposta = modelo.invoke(prompt)
print(resposta)
