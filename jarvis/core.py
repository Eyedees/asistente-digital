#entra un mensaje y devuelve un mensaje de respuesta, usando el modelo de lenguaje
#NUNCA LLAMA A input() NI print(), SOLO DEVUELVE UN MENSAJE DE RESPUESTA

from jarvis.llm import generar

SYSTEM_PROMPT = (
    "Eres un asistente personal. "
    "Responde en español, de forma directa y sin rodeos."
)
MAX_MENSAJES = 20  # par: cada intercambio son 2 mensajes (usuario + asistente)


class Asistente:
    def __init__(self):
        self.historial = []  # memoria de trabajo: dura mientras el programa esté abierto

    def responder(self, mensaje):
        mensajes = [{"role": "system", "content": SYSTEM_PROMPT}]
        mensajes += self.historial
        mensajes.append({"role": "user", "content": mensaje})

        partes = []
        for trozo in generar(mensajes):
            partes.append(trozo)
            yield trozo

        respuesta = "".join(partes)
        if respuesta:  # si el modelo no devolvió texto, no ensuciamos el historial
            self.historial += [
                {"role": "user", "content": mensaje},
                {"role": "assistant", "content": respuesta},
            ]
            self.historial = self.historial[-MAX_MENSAJES:]