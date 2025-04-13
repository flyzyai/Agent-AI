import os
import openai

# Nowa funkcja do zapytań do OpenAI, asynchroniczna
async def ask_ai(message: str) -> str:
    try:
        # Wywołanie OpenAI z API ChatCompletion
        response = await openai.ChatCompletion.create(  # Zmiana na asynchroniczną funkcję
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Wystąpił błąd przy zapytaniu do OpenAI: {e}"
