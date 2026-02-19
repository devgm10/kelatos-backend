import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_and_summarize(message: str) -> dict:

    prompt = f"""
    1. Clasifica el siguiente mensaje en una de estas categorías:
        Ventas, Soporte, Información o Spam.

    2. Luego genera un resumen simulando que eres el usuario (1 oración).

    3. Devuelve SOLO un JSON válido con este formato exacto:
    {{
        "category": "Ventas|Soporte|Información|Spam",
        "summary": "texto"
    }}

    Mensaje:
    {message}
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    content = response.output_text.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "category": "Información",
            "summary": content[:120]
        }


def assign_priority(category: str) -> str:
    mapping = {
        "Ventas": "Media",
        "Soporte": "Alta",
        "Imformación": "Media",
        "Spam": "Baja"
    }

    return mapping.get(category, "Media")