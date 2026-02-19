reviews = ["Eu gostei bastante da câmera é a primeira vez que eu tiro foto com câmeras tirei algumas fotos não de pessoas no momento mas de algum objeto vou postar pra vocês verem",
           "Perfect!!! top de linha, vem com tudo que é descrito e ganhei um brinde maravilhoso. Verifiquei tudo, procedência etc etc. Tudo ok, não vão se arrepender!.",
           "Uma das melhores câmeras custo benefício para iniciantes da canon. Boa conectividade. Facilidade de aprender a mexer. Vale a pena pra quem não quer gastar muito mas quer ter câmera semi profissional.",
           "A apresentação da câmera é muito boa, mas preciso de uma câmera menor e mais compacta."]


from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class Avaliacao(BaseModel):
    "Review foi enviado por um cliente que comprou um produto, preciso avaliar esse produto para saber se ele é bom e se vale a pena, identificar os pontos positivos e negativos do produto, e se a avaliação é positiva ou negativa."
    review_positiva: bool = Field(description="essa avaliação foi positiva ou negativa?")
    vale_pena: bool = Field(description="Essa avaliação no geral diz que vale a pena ou não vale a pena comprar esse produto?")
    pontos_positivos: list[str] = Field(description="quais os principais pontos positivos dessa avaliação? (cada ponto em no máximo 3 palavras, se houver)")
    pontos_negativos: list[str] = Field(description="quais os principais pontos negativos dessa avaliação? (cada ponto em no máximo 3 palavras, se houver)")
    
class AvaliacoesList(BaseModel):
    avaliacoes: list[Avaliacao] = Field(description="lista de avaliações extraídas dos reviews")
    
parser = JsonOutputParser(name="avaliacao_usuario", pydantic_object=AvaliacoesList)
instrucoes = parser.get_format_instructions()


context_template = PromptTemplate.from_template("Você está avaliando reviews de varios usuários sobre um produto, preciso de algumas informações extraídas desses reviews: {reviews}")
language_template = PromptTemplate.from_template("Responda sempre em {idioma}", partial_variables={"idioma": "português"})
format_template = PromptTemplate.from_template("Formato da resposta: {formato}", partial_variables={"formato": instrucoes})
final_template = ( context_template + language_template + format_template)

modelo = ChatOpenAI()
prompt = final_template.invoke({"reviews": reviews})
resposta = modelo.invoke(prompt)
resposta = parser.invoke(resposta)
print(resposta)
    
