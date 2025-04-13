import os
import httpx
import logging
from fastapi import Request, HTTPException

# Ustawienia tokenu Telegrama
TELEGRAM_TOKEN = os.getenv("7439037241:AAFKc-0JRGMebKpa37Bp5dDfN9MYEkQ3XqQ")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Funkcja wysyłania wiadomości do użytkownika
async def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={"chat_id": chat_id, "text": text})
            if response.status_code != 200:
                logging.error(f"Error sending message: {response.status_code} - {response.text}")
            else:
                logging.info(f"Message sent to {chat_id}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

# Funkcja obsługująca zapytania przychodzące z Telegrama
async def handle_telegram_update(request: Request, ask_ai_fn):
    try:
        # Odczytanie ciała zapytania
        body = await request.json()
        logging.info(f"Received update: {body}")

        # Pobranie wiadomości i chat_id
        message = body.get("message", {}).get("text", "")
        chat_id = body.get("message", {}).get("chat", {}).get("id", "")

        # Sprawdzenie, czy wiadomość i chat_id są poprawne
        if not message or not chat_id:
            logging.error("Invalid message or chat_id received.")
            raise HTTPException(status_code=400, detail="Invalid message or chat_id")

        # Przesłanie wiadomości do AI i uzyskanie odpowiedzi
        ai_response = await ask_ai_fn(message)  # Zakładając, że ask_ai_fn jest asynchroniczne
        if ai_response:
            # Wysłanie odpowiedzi do użytkownika
            await send_message(chat_id, ai_response)
        else:
            logging.warning("AI response is empty.")

        return {"ok": True}

    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
