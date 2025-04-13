import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Asynchroniczna funkcja, która wysyła zapytanie do OpenAI
async def ask_ai(message: str) -> str:
    try:
        # Wywołanie nowej wersji API (asynchronicznie)
        response = await openai.ChatCompletion.acreate(  # Używamy 'acreate' dla asynchronicznego wywołania
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message['content'].strip()  # Zwracamy treść odpowiedzi
    except Exception as e:
        return f"Wystąpił błąd przy zapytaniu do OpenAI: {e}"
