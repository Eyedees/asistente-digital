from types import SimpleNamespace

import jarvis.llm as llm


class _Chunk:
    def __init__(self, texto):
        self.choices = [SimpleNamespace(delta=SimpleNamespace(content=texto))]


def test_generar_hace_streaming_y_filtra_trozos_vacios(monkeypatch):
    capturado = {}

    def crear(**kwargs):
        capturado.update(kwargs)
        return iter([_Chunk("Hola"), _Chunk(None), _Chunk(" mundo")])

    monkeypatch.setattr(llm._client.chat.completions, "create", crear)

    trozos = list(llm.generar([{"role": "user", "content": "hola"}]))

    assert trozos == ["Hola", " mundo"]
    assert capturado["model"] == "openai/gpt-oss-120b"
    assert capturado["messages"] == [{"role": "user", "content": "hola"}]
    assert capturado["stream"] is True
