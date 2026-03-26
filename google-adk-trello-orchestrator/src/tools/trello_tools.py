import os
from tools.trello_api import fetch_cards, fetch_lists, move_card

BOARD_ID = os.getenv("TRELLO_BOARD_ID")


def listar_cards_tool() -> str:
    cards = fetch_cards(BOARD_ID)

    if not cards:
        return "Nenhum card encontrado."

    resultado = "📋 Lista de tarefas:\n"

    for card in cards:
        resultado += f"- {card['name']}\n"

    return resultado


def concluir_card_tool(nome: str) -> str:
    """
    Move um card para a lista de conclusão.
    """

    # guardrail
    if not nome or len(nome) < 3:
        return "❌ Nome de tarefa inválido."

    cards = fetch_cards(BOARD_ID)
    lists = fetch_lists(BOARD_ID)

    # IMPORTANTE → não sobrescrever 'nome'
    lista_done = None
    for l in lists:
        nome_lista = l["name"].lower()  # variável separada
        if nome_lista in ["done", "concluido", "concluído"]:
            lista_done = l["id"]
            print(f"[DEBUG] Lista encontrada: {l['name']}")
            break

    if not lista_done:
        return "❌ Não encontrei uma coluna de conclusão."

    # DEBUG IMPORTANTE
    print(f"[DEBUG] Buscando card com nome: {nome}")

    for card in cards:
        print(f"[DEBUG] Comparando com: {card['name']}")

        if nome.lower() in card["name"].lower():
            move_card(card["id"], lista_done)
            return f"✅ Card '{card['name']}' concluído."

    return f"❌ Card '{nome}' não encontrado."