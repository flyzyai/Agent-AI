from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai_agent import ask_ai
from flight_api import search_flights
from telegram_bot import handle_telegram_update

app = FastAPI()

class Query(BaseModel):
    message: str

# Endpoint GET do sprawdzenia działania aplikacji
@app.get("/")  
async def read_root():
    return {"message": "Server is running"}

# Endpoint POST do zadawania pytań do OpenAI
@app.post("/ask")
async def ask(query: Query):
    ai_response = await ask_ai(query.message)  # Asynchronicznie wysyłamy zapytanie do OpenAI
    flights = search_flights(ai_response)  # Wyniki lotów na podstawie odpowiedzi AI
    return {"flights": flights, "ai_response": ai_response}

# Endpoint webhook do obsługi wiadomości z Telegrama
@app.post("/webhook")
async def telegram_webhook(request: Request):
    return await handle_telegram_update(request)  # Obsługuje webhook i przekazuje dane do funkcji
