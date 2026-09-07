# Asistente Digital

Asistente conversacional de IA con interfaz de línea de comandos, construido en Python. Utiliza la API de Groq para inferencia en tiempo real (streaming) sobre modelos de lenguaje de código abierto.

Este proyecto forma parte de mi portfolio como muestra de integración con APIs externas, manejo seguro de credenciales y diseño incremental de software.

## Características

- 💬 Conversación por consola en tiempo real (respuesta en streaming, token a token)
- 🔐 Gestión segura de credenciales mediante variables de entorno
- 🔄 Bucle de conversación continuo
- 🧠 Modelo: `openai/gpt-oss-120b` (razonamiento + baja latencia vía Groq)

## Stack técnico

| Componente        | Tecnología           |
|-------------------|----------------------|
| Lenguaje          | Python 3.14          |
| Proveedor de LLM  | Groq API             |
| Modelo            | openai/gpt-oss-120b  |
| Gestión de config | python-dotenv        |

## Requisitos previos

- Python 3.10 o superior
- Una cuenta en [Groq Console](https://console.groq.com) con una API key generada

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/asistente-digital.git
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

4. Crea un archivo `.env` en la raíz del proyecto con tu clave de API:

   ```
   GROQ_API_KEY=tu_clave_aqui
   ```

## Uso

Con el entorno virtual activado:

```bash
python main.py
```

El programa te pedirá que escribas tu petición. La respuesta se imprime en tiempo real. El ciclo se repite indefinidamente hasta que el usuario interrumpe la ejecución con `Ctrl + C`.

## Estructura del proyecto

```
asistente-digital/
├── main.py              # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias del proyecto
├── .env                  # Variables de entorno (no versionado)
├── .gitignore
└── README.md
```

## Variables de entorno

| Variable        | Descripción                              | Requerida |
|-----------------|-------------------------------------------|-----------|
| `GROQ_API_KEY`  | Clave de autenticación para la API de Groq | Sí        |

> ⚠️ El archivo `.env` está excluido del control de versiones mediante `.gitignore`. Nunca subas tus credenciales a un repositorio público.

## Roadmap

- [x] Fase 1 — Asistente de texto en consola con streaming
- [ ] Fase 2 — Memoria conversacional (historial de mensajes)
- [ ] Fase 3 — Entrada por voz (speech-to-text)
- [ ] Fase 4 — Salida por voz (text-to-speech)
- [ ] Fase 5 — Interfaz gráfica

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

Desarrollado por [Tu Nombre] como parte de su portfolio de ingeniería de software.
