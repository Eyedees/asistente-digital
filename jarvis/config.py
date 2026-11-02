#único sitio que lee .env y configura logs
#NINGÚN OTRO ARCHIVO DEBE LEER .ENV NI CONFIGURAR LOGS, SOLO ESTE ARCHIVO

import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Falta GROQ_API_KEY en .env (usa .env.example como plantilla).")

# Entrada por voz (opcionales). El modelo se descarga la primera vez.
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "auto")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "es")