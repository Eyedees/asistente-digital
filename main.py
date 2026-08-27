from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()
while True:
    print("\n" + "_" * 80 + "\n")
    mensaje = input("Escribe aquí tu petición: ")
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
        {
            "role": "user",
            "content": mensaje
        }
        ],
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )
    print("\n")
    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="", flush=True)