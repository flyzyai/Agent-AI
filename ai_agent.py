import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_ai(message):
    prompt = f"""
    Na podstawie tej wiadomości użytkownika, wyodrębnij dane podróży:
    Wiadomość: {message}
    Zwróć JSON w formacie:
    {{
        "origin": "...",
        "destination": "...",
        "date": "...",
        "budget": "..."
    }}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
