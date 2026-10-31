#interfaz de consola: lee la entrada del usuario e imprime la respuesta en streaming

from jarvis.core import Asistente


def main():
    asistente = Asistente()
    print("Escribe 'salir' para terminar o 'borrar memoria' para borrar el historial.")
    while True:
        try:
            print("\n" + "_" * 80 + "\n")
            mensaje = input("Escribe aquí tu petición: ").strip()
            if not mensaje:
                continue
            if mensaje.lower() in ("salir", "exit"):
                break
            print("\n")
            if mensaje.lower() == "borrar memoria":
                respuesta = input(
                    "¿Estás seguro de que quieres borrar la memoria? (s/n): "
                ).strip().lower()
                if respuesta in ("s", "si", "sí"):
                    asistente.borrar_memoria()
                    print("\nMemoria borrada. Empezamos de cero.")
                else:
                    print("\nMemoria no borrada. Continuamos con el historial existente.")
                continue
            for trozo in asistente.responder(mensaje):
                print(trozo, end="", flush=True)

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"\n[Error: {e}]")
    print("\nGero Arte!\n")
