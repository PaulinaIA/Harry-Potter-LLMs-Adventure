import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVES_DIR = os.path.join(DATA_DIR, "saves")

# Configuración del modelo
MODEL = "llama3.2:1b"
OPENAI_BASE_URL = "http://127.0.0.1:11434/v1"
OPENAI_API_KEY = "ollama"

# Ajustes del juego
MAX_SAVE_SLOTS = 5
AUTOSAVE_INTERVAL = 300  # segundos