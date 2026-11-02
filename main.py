import argparse

from jarvis.interfaces.cli import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asistente Digital")
    parser.add_argument(
        "--voz",
        action="store_true",
        help="Inicia el asistente en modo voz",
    )
    args = parser.parse_args()
    main(voz_inicial=args.voz)
