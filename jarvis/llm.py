#llamada al modelo de lenguaje
#es el único archivo que sabe qué proveedor y modelo se usan, y cómo se llama a la API


from groq import Groq

from jarvis.config import GROQ_API_KEY

_client = Groq(api_key=GROQ_API_KEY)


def generar(mensajes):
    """Recibe la lista de mensajes y devuelve la respuesta en trozos de texto."""
    completion = _client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=mensajes,
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None,
    )
    for chunk in completion:
        texto = chunk.choices[0].delta.content
        if texto:
            yield texto