import os

import pytest

# Evita que los tests necesiten una GROQ_API_KEY real.
os.environ.setdefault("GROQ_API_KEY", "test-key")

import jarvis.memoria as memoria


@pytest.fixture
def db_temporal(tmp_path, monkeypatch):
    """Redirige la base de datos a un directorio temporal por test."""
    ruta = tmp_path / "data" / "asistente.db"
    monkeypatch.setattr(memoria, "RUTA_DB", ruta)
    return ruta
