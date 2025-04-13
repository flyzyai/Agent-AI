import os
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Wystąpił błąd przy zapytaniu do OpenAI: {e}"
