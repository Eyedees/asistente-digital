#interfaz de consola: lee la entrada del usuario e imprime la respuesta en streaming

from jarvis.core import Asistente
from jarvis.voz import grabar_y_transcribir

SEPARADOR = "\n" + "_" * 80 + "\n"


def _responder(asistente, mensaje):
    for trozo in asistente.responder(mensaje):
        print(trozo, end="", flush=True)


def _confirmar_borrado(asistente):
    respuesta = input(
        "¿Estás seguro de que quieres borrar la memoria? (s/n): "
    ).strip().lower()
    if respuesta in ("s", "si", "sí"):
        asistente.borrar_memoria()
        print("\nMemoria borrada. Empezamos de cero.")
    else:
        print("\nMemoria no borrada. Continuamos con el historial existente.")


def _escuchar():
    try:
        texto = grabar_y_transcribir()
    except Exception as e:
        print(f"\n[Error de voz: {e}]")
        return None
    if texto:
        print(f"Tú (voz): {texto}")
    return texto


def main(voz_inicial=False):
    asistente = Asistente()
    if voz_inicial:
        print("Modo voz. Pulsa Enter para hablar o escribe 'salir' para terminar.")
    else:
        print(
            "Escribe 'salir' para terminar, 'voz' para hablar "
            "o 'borrar memoria' para borrar el historial."
        )

    while True:
        try:
            print(SEPARADOR)

            if voz_inicial:
                orden = input(
                    "Pulsa Enter para hablar, o escribe 'salir': "
                ).strip()
                if orden.lower() in ("salir", "exit"):
                    break
                mensaje = orden if orden else _escuchar()
            else:
                mensaje = input("Escribe aquí tu petición: ").strip()
                if not mensaje:
                    continue
                if mensaje.lower() in ("salir", "exit"):
                    break
                if mensaje.lower() == "voz":
                    mensaje = _escuchar()

            if mensaje is None:
                continue
            if not mensaje:
                print("No se ha detectado voz. Inténtalo de nuevo.")
                continue
            if mensaje.lower() in ("salir", "exit"):
                break
            if mensaje.lower() == "borrar memoria":
                _confirmar_borrado(asistente)
                continue

            print("\n")
            _responder(asistente, mensaje)
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"\n[Error: {e}]")
    print("\nGero Arte!\n")
