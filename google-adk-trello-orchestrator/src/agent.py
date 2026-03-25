import os
from google import genai
from tools.trello_tools import listar_cards_tool, concluir_card_tool
from dotenv import load_dotenv

load_dotenv()

# ✅ NOVO PADRÃO
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def decidir_acao(user_input: str) -> str:
    """
    O LLM decide qual tool usar baseado na intenção.
    """

    prompt = f"""
    Você é um agente que controla o Trello.

    Você pode:
    1. Listar tarefas
    2. Concluir tarefas

    Regras:
    - Se o usuário pedir para listar → responda: LISTAR
    - Se pedir para concluir → responda: CONCLUIR: nome_da_tarefa

    Responda apenas no formato:

    LISTAR
    ou
    CONCLUIR: nome_da_tarefa

    Entrada do usuário:
    {user_input}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    # Compatível com nova API
    try:
        return response.text.strip()
    except:
        return response.candidates[0].content.parts[0].text.strip()


def executar_acao(decisao: str) -> str:
    """
    Executa a tool baseada na decisão do LLM.
    """

    if decisao == "LISTAR":
        return listar_cards_tool()

    if decisao.startswith("CONCLUIR:"):
        nome = decisao.replace("CONCLUIR:", "").strip()
        return concluir_card_tool(nome)

    return "❌ Não entendi a ação."


def agent(user_input: str) -> str:
    decisao = decidir_acao(user_input)
    print(f"[DEBUG decisão]: {decisao}")
    return executar_acao(decisao)