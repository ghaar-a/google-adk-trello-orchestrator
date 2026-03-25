import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")

def fetch_cards(board_id):
    """Busca todos os cards de um board."""
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    query = {'key': API_KEY, 'token': TOKEN}
    response = requests.get(url, params=query)
    response.raise_for_status()
    return response.json()


def fetch_lists(board_id):
    """Busca todas as listas de um board."""
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    query = {'key': API_KEY, 'token': TOKEN}
    response = requests.get(url, params=query)
    response.raise_for_status()
    return response.json()


def move_card(card_id, list_id):
    """Move um card para outra lista."""
    url = f"https://api.trello.com/1/cards/{card_id}"
    query = {'idList': list_id, 'key': API_KEY, 'token': TOKEN}
    response = requests.put(url, params=query)
    response.raise_for_status()
    return response.json()