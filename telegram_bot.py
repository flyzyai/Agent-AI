from fastapi import Request
import requests
import os
import openai
from ai_agent import ask_ai  # Importuj asynchroniczną funkcję

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Funkcja wysyłająca wiadomość na Telegram
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# Obsługuje webhooki z Telegrama
async def handle_telegram_update(request: Request, ask_ai_fn):
    body = await request.json()  # Asynchroniczne odczytanie danych z webhooka
    message = body.get("message", {}).get("text", "")
    chat_id = body.get("message", {}).get("chat", {}).get("id", "")

    if message and chat_id:
        ai_response = await ask_ai_fn(message)  # Używamy 'await' dla asynchronicznej funkcji
        send_message(chat_id, ai_response)

    return {"ok": True}
