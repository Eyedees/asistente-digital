import importlib

import pytest

import jarvis.config as config


def test_falla_si_no_hay_api_key(monkeypatch):
    monkeypatch.setattr(config.os, "getenv", lambda _: None)
    try:
        with pytest.raises(RuntimeError, match="GROQ_API_KEY"):
            importlib.reload(config)
    finally:
        monkeypatch.undo()
        importlib.reload(config)
