import os
import requests
from fastapi import Request
from ai_agent import ask_ai  # Importujemy funkcję asynchroniczną
import logging

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Funkcja do wysyłania wiadomości do Telegrama
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    response = requests.post(url, json={"chat_id": chat_id, "text": text})
    logging.info(f"Telegram response: {response.json()}")  # Logowanie odpowiedzi z Telegrama

# Funkcja obsługująca webhook Telegrama
async def handle_telegram_update(request: Request):
    logging.info("Received webhook request")  # Logowanie, że webhook został otrzymany
    body = await request.json()  # Oczekujemy asynchronicznego odczytu danych
    logging.info(f"Request body: {body}")  # Logowanie ciała zapytania

    message = body.get("message", {}).get("text", "")
    chat_id = body.get("message", {}).get("chat", {}).get("id", "")

    if message and chat_id:
        logging.info(f"Received message: {message} from chat_id: {chat_id}")  # Logowanie otrzymanej wiadomości
        ai_response = await ask_ai(message)  # Asynchroniczne zapytanie do OpenAI
        logging.info(f"AI response: {ai_response}")  # Logowanie odpowiedzi od AI
        send_message(chat_id, ai_response)  # Wysyłamy odpowiedź do Telegrama
    else:
        logging.warning("No message or chat_id found in the request body.")  # Logowanie ostrzeżenia, jeśli brakuje wiadomości lub chat_id

    return {"ok": True}
