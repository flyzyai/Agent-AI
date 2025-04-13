import os
import requests
from fastapi import Request

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

async def handle_telegram_update(request: Request, ask_ai_fn):
    body = await request.json()
    message = body.get("message", {}).get("text", "")
    chat_id = body.get("message", {}).get("chat", {}).get("id", "")

    if message and chat_id:
        ai_response = ask_ai_fn(message)
        send_message(chat_id, ai_response)

    return {"ok": True}
