import json
import os
import time
from pathlib import Path


class GameState:
    def __init__(self, saves_dir):
        self.saves_dir = saves_dir
        self.attributes = {}
        self.inventory = []
        self.history = []
        self.house = ""
        self.character_name = ""
        self.last_save = 0

        # Asegurar que exista el directorio de guardado
        os.makedirs(self.saves_dir, exist_ok=True)

    def save(self, slot=0, name=None):
        """Guarda el estado actual del juego"""
        filename = f"save_{slot}.json"
        if name:
            filename = f"save_{slot}_{name.replace(' ', '_')}.json"

        filepath = os.path.join(self.saves_dir, filename)

        data = {
            "timestamp": time.time(),
            "save_name": name or f"Partida {slot}",
            "attributes": self.attributes,
            "inventory": self.inventory,
            "history": self.history,
            "house": self.house,
            "character_name": self.character_name
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.last_save = time.time()
        return filepath

    def load(self, slot=0):
        """Carga un estado guardado del juego"""
        pattern = f"save_{slot}"

        for filename in os.listdir(self.saves_dir):
            if filename.startswith(pattern) and filename.endswith(".json"):
                filepath = os.path.join(self.saves_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.attributes = data.get("attributes", {})
                self.inventory = data.get("inventory", [])
                self.history = data.get("history", [])
                self.house = data.get("house", "")
                self.character_name = data.get("character_name", "")

                return True

        return False

    def get_save_slots(self):
        """Obtiene información sobre todas las partidas guardadas"""
        saves = []

        for filename in os.listdir(self.saves_dir):
            if filename.startswith("save_") and filename.endswith(".json"):
                filepath = os.path.join(self.saves_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    slot = int(filename.split("_")[1].split(".")[0])
                    saves.append({
                        "slot": slot,
                        "name": data.get("save_name", f"Partida {slot}"),
                        "timestamp": data.get("timestamp", 0),
                        "house": data.get("house", ""),
                        "character": data.get("character_name", "Desconocido"),
                        "filepath": filepath
                    })
                except Exception as e:
                    print(f"Error al leer {filepath}: {e}")

        return sorted(saves, key=lambda x: x["slot"])