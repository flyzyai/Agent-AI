import os
import httpx
import logging
from fastapi import Request, HTTPException

# Ustawienie poziomu logowania na INFO, aby widzieć więcej informacji w logach
logging.basicConfig(level=logging.INFO)

# Pobranie tokenu bota Telegrama z zmiennych środowiskowych (zalecane trzymanie tokenu w pliku .env)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    logging.error("Brak tokenu bota Telegrama! Upewnij się, że zmienna środowiskowa TELEGRAM_BOT_TOKEN jest ustawiona.")
    raise Exception("Brak tokenu bota Telegrama!")

# Budowanie URL API bota Telegrama na podstawie tokenu
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Funkcja wysyłania wiadomości do użytkownika na Telegramie
async def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    
    # Wysyłanie zapytania POST do API Telegrama za pomocą httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={"chat_id": chat_id, "text": text})
            if response.status_code != 200:
                logging.error(f"Błąd podczas wysyłania wiadomości: {response.status_code} - {response.text}")
            else:
                logging.info(f"Wiadomość wysłana do chat_id: {chat_id}")
        except Exception as e:
            logging.error(f"Błąd podczas wysyłania wiadomości: {e}")

# Funkcja obsługująca aktualizacje przychodzące od Telegrama (webhook)
async def handle_telegram_update(request: Request, ask_ai_fn):
    try:
        # Odczytanie ciała zapytania w formacie JSON
        body = await request.json()
        logging.info(f"Otrzymano update: {body}")

        # Pobranie wiadomości i chat_id z treści zapytania
        message = body.get("message", {}).get("text", "")
        chat_id = body.get("message", {}).get("chat", {}).get("id", "")

        # Sprawdzenie, czy wiadomość i chat_id są poprawnie pobrane
        if not message or not chat_id:
            logging.error("Błąd: brak wiadomości lub chat_id.")
            raise HTTPException(status_code=400, detail="Brak wiadomości lub chat_id")

        # Przesyłanie wiadomości do AI w celu uzyskania odpowiedzi
        ai_response = await ask_ai_fn(message)  # Zakładamy, że ask_ai_fn jest asynchroniczne
        if ai_response:
            # Jeśli odpowiedź AI nie jest pusta, wysyłamy ją do użytkownika
            await send_message(chat_id, ai_response)
        else:
            logging.warning("Odpowiedź AI jest pusta.")

        return {"ok": True}  # Zwracamy odpowiedź potwierdzającą poprawne przetworzenie webhooka

    except Exception as e:
        # Logowanie błędów w przypadku wystąpienia problemu
        logging.error(f"Błąd podczas przetwarzania webhooka: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Błąd serwera")

