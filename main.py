from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai_agent import ask_ai
from flight_api import search_flights
from telegram_bot import handle_telegram_update

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    ai_response = ask_ai(query.message)
    flights = search_flights(ai_response)
    return {"flights": flights, "ai_response": ai_response}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    return await handle_telegram_update(request, ask_ai)
