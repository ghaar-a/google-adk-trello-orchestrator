import os
import json
import re  # para limpar resposta
from google import genai
from tools.trello_tools import listar_cards_tool, concluir_card_tool
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extrair_json(texto: str) -> dict:
    """
     Extrai JSON mesmo se vier com texto extra
    """
    try:
        # tenta direto
        return json.loads(texto)
    except:
        pass

    # tenta encontrar JSON dentro do texto
    match = re.search(r"\{.*\}", texto, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return {"tool": "desconhecido"}


def decidir_acao(user_input: str) -> dict:
    """
    Decide qual tool usar via LLM
    """

    prompt = f"""
    Você é um agente que controla o Trello.

    Ferramentas disponíveis:
    - listar_cards
    - concluir_card (argumento: nome)

    REGRAS:
    - Responda APENAS com JSON
    - NÃO escreva texto antes ou depois

    Exemplos válidos:

    {{ "tool": "listar_cards" }}

    {{ "tool": "concluir_card", "args": {{ "nome": "comprar pão" }} }}

    Entrada:
    {user_input}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # ATUALIZADO
            contents=prompt
        )

        try:
            text = response.text
        except:
            text = response.candidates[0].content.parts[0].text

        print(f"[DEBUG RAW LLM]: {text}")  # IMPORTANTE

        return extrair_json(text)

    except Exception as e:
        print(f"[ERRO LLM]: {str(e)}")
        return {"tool": "desconhecido"}


# TOOL REGISTRY
TOOLS = {
    "listar_cards": listar_cards_tool,
    "concluir_card": concluir_card_tool
}


def executar_acao(decisao: dict) -> str:
    tool_name = decisao.get("tool")

    if tool_name == "desconhecido":
        return "⚠️ Falha ao interpretar resposta da IA."

    tool = TOOLS.get(tool_name)

    if not tool:
        return "❌ Tool não encontrada."

    args = decisao.get("args", {})

    try:
        return tool(**args) if args else tool()
    except Exception as e:
        return f"❌ Erro ao executar a tool: {str(e)}"


def agent(user_input: str) -> str:
    decisao = decidir_acao(user_input)
    print(f"[DEBUG TOOL CALL]: {decisao}")
    return executar_acao(decisao)