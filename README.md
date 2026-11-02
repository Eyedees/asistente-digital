# Asistente Digital

Asistente conversacional de IA con interfaz de línea de comandos, construido en Python. Utiliza la API de Groq para inferencia en tiempo real (streaming) sobre modelos de lenguaje de código abierto.

Este proyecto forma parte de mi portfolio como muestra de integración con APIs externas, manejo seguro de credenciales y diseño incremental de software.

## Características

- 💬 Conversación por consola en tiempo real (respuesta en streaming, token a token)
- 🧠 Memoria conversacional persistente en SQLite (recupera el historial entre sesiones)
- ✂️ Contexto acotado a los últimos 20 mensajes para controlar tokens y latencia
- 🔐 Gestión segura de credenciales mediante variables de entorno
- 🧩 Arquitectura modular: configuración, cliente LLM, lógica de negocio e interfaz separados
- 🧪 Suite de tests con `pytest` (sin llamadas reales a la API)
- 🔄 Bucle de conversación continuo
- 🤖 Modelo: `openai/gpt-oss-120b` (razonamiento + baja latencia vía Groq)

## Stack técnico

| Componente        | Tecnología           |
|-------------------|----------------------|
| Lenguaje          | Python 3.14          |
| Proveedor de LLM  | Groq API             |
| Modelo            | openai/gpt-oss-120b  |
| Gestión de config | python-dotenv        |
| Persistencia      | SQLite (stdlib)      |
| Tests             | pytest               |

## Requisitos previos

- Python 3.10 o superior
- Una cuenta en [Groq Console](https://console.groq.com) con una API key generada

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Eyedees/asistente-digital.git
   cd asistente-digital
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   ```

   En Windows (PowerShell):

   ```powershell
   & ".\venv\Scripts\activate"
   ```

   En macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea tu archivo `.env` a partir de la plantilla y añade tu clave:

   ```bash
   cp .env.example .env
   ```

   En Windows (PowerShell):

   ```powershell
   Copy-Item .env.example .env
   ```

   Después edita `.env` y rellena el valor:

   ```
   GROQ_API_KEY=tu_clave_aqui
   ```

## Uso

Con el entorno virtual activado:

```bash
python main.py
```

El programa te pedirá que escribas tu petición. La respuesta se imprime en tiempo real. Escribe `salir` (o `exit`), o pulsa `Ctrl + C`, para terminar. El historial se conserva entre ejecuciones en `data/asistente.db`.

Para vaciar el historial desde la propia aplicación, escribe `borrar memoria` (pedirá confirmación).

## Tests

La suite usa `pytest` y no realiza llamadas reales a Groq: el modelo y la base de datos se sustituyen por dobles de prueba.

Ejecuta los tests **desde la raíz del proyecto** y con su entorno virtual activado:

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## Estructura del proyecto

```
asistente-digital/
├── main.py                  # Punto de entrada de la aplicación
├── jarvis/
│   ├── __init__.py
│   ├── config.py            # Carga y validación de variables de entorno
│   ├── llm.py               # Cliente de Groq y streaming del modelo
│   ├── core.py              # Lógica del asistente y gestión del historial
│   ├── memoria.py           # Persistencia del historial en SQLite
│   └── interfaces/
│       ├── __init__.py
│       └── cli.py           # Interfaz de línea de comandos
├── tests/                   # Pruebas automatizadas
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_core.py
│   └── test_memoria.py
├── data/                    # Historial local en SQLite (se crea al ejecutar)
├── requirements.txt         # Dependencias del proyecto
├── requirements-dev.txt     # Dependencias de desarrollo (pytest)
├── pytest.ini               # Configuración de pytest
├── .env.example             # Plantilla de variables de entorno
├── .gitignore
├── LICENSE
└── README.md
```

### Flujo de una petición

```
main.py → interfaces/cli.py → core.Asistente → llm.generar → Groq API
                                    ↕
                              memoria.py (SQLite)
```

Cada capa tiene una única responsabilidad: la CLI lee y escribe en consola, `core` construye el contexto y gestiona el historial, `memoria` lo persiste en disco, `llm` habla con el proveedor y `config` centraliza la configuración.

## Memoria

El historial se guarda en `data/asistente.db`, una base de datos SQLite que se crea automáticamente la primera vez que se ejecuta el programa.

- Al arrancar, se cargan en contexto los **últimos 20 mensajes**; el resto permanece en disco sin consumir tokens.
- Cada intercambio (pregunta + respuesta) se guarda al terminar la respuesta.
- `data/` está incluido en `.gitignore`: tus conversaciones no se versionan ni se suben al repositorio.
- Para vaciar el historial, escribe `borrar memoria` dentro de la aplicación (pide confirmación). También puedes eliminar `data/asistente.db`.

## Variables de entorno

| Variable        | Descripción                                | Requerida |
|-----------------|--------------------------------------------|-----------|
| `GROQ_API_KEY`  | Clave de autenticación para la API de Groq | Sí        |

> ⚠️ El archivo `.env` está excluido del control de versiones mediante `.gitignore`. Nunca subas tus credenciales a un repositorio público.

## Roadmap

- [x] Fase 1 — Asistente de texto en consola con streaming
- [x] Fase 2 — Memoria conversacional persistente (SQLite)
- [ ] Fase 3 — Entrada por voz (speech-to-text)
- [ ] Fase 4 — Salida por voz (text-to-speech)
- [ ] Fase 5 — Interfaz gráfica

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor

Desarrollado por **Eyedees** ([@Eyedees](https://github.com/Eyedees)) como parte de su portfolio de ingeniería de software.
