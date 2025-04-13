import os
import requests
from fastapi import Request
from ai_agent import ask_ai  # Importujemy asynchroniczną funkcję

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Funkcja do wysyłania wiadomości
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# Obsługuje webhooki Telegrama, wykonując zapytanie do OpenAI
async def handle_telegram_update(request: Request):
    body = await request.json()  # Oczekujemy asynchronicznego odczytu danych
    message = body.get("message", {}).get("text", "")
    chat_id = body.get("message", {}).get("chat", {}).get("id", "")

    if message and chat_id:
        ai_response = await ask_ai(message)  # Wykorzystujemy 'await' dla asynchronicznej funkcji
        send_message(chat_id, ai_response)  # Odpowiedź wysyłana do Telegrama

    return {"ok": True}
