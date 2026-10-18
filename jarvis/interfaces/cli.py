#chat por texto que ya existe en main.py, pero se puede mover a este archivo si se desea

from jarvis.core import Asistente


def main():
    asistente = Asistente()
    print("Escribe 'salir' para terminar.")
    while True:
        try:
            print("\n" + "_" * 80 + "\n")
            mensaje = input("Escribe aquí tu petición: ").strip()
            if not mensaje:
                continue
            if mensaje.lower() in ("salir", "exit"):
                break
            print("\n")
            for trozo in asistente.responder(mensaje):
                print(trozo, end="", flush=True)
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"\n[Error: {e}]")
    print("\nHasta luego.")