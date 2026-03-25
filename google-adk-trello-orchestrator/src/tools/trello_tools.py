import os
from tools.trello_api import fetch_cards, fetch_lists, move_card

BOARD_ID = os.getenv("TRELLO_BOARD_ID")


def listar_cards_tool() -> str:
    """
    Lista todos os cards do Trello de forma amigável para o agente.
    """
    cards = fetch_cards(BOARD_ID)

    if not cards:
        return "Nenhum card encontrado."

    resultado = "📋 Lista de tarefas:\n"
    for card in cards:
        resultado += f"- {card['name']}\n"

    return resultado


def concluir_card_tool(nome_card: str) -> str:
    """
    Move um card para a lista 'Done' baseado no nome.
    """
    cards = fetch_cards(BOARD_ID)
    lists = fetch_lists(BOARD_ID)

    # encontrar lista DONE (última)
    lista_done = lists[-1]["id"]

    # buscar card pelo nome
    for card in cards:
        if nome_card.lower() in card["name"].lower():
            move_card(card["id"], lista_done)
            return f"✅ Card '{card['name']}' movido para Done."

    return f"❌ Card '{nome_card}' não encontrado."