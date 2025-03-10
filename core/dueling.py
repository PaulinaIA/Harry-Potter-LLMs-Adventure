# core/dueling.py
class DuelingSystem:
    def __init__(self, game_state):
        self.state = game_state
        self.spells = {
            "expelliarmus": {"power": 3, "type": "defensa", "description": "Desarma a tu oponente"},
            "stupefy": {"power": 4, "type": "ataque", "description": "Aturde a tu oponente"},
            "protego": {"power": 2, "type": "defensa", "description": "Crea un escudo protector"},
            "expecto patronum": {"power": 5, "type": "defensa", "description": "Invoca un patronus protector"},
            "petrificus totalus": {"power": 3, "type": "ataque", "description": "Petrifica a tu oponente"}
        }

    def duel(self, player_spell, opponent_name="Estudiante", difficulty=1):
        # Verificar si el hechizo existe
        spell_info = self.spells.get(player_spell.lower(), None)

        if not spell_info:
            return f"No conoces el hechizo '{player_spell}'. Prueba con otro."

        # Calcular resultado del duelo
        spell_power = spell_info["power"]
        attribute_bonus = min(self.state.attributes.get("valentía", 0) / 2, 5)
        player_power = spell_power + attribute_bonus

        # Determinar poder del oponente
        opponent_power = 2 * difficulty

        # Resultado del duelo
        if player_power > opponent_power:
            # Añadir al inventario si corresponde
            if spell_info["type"] == "ataque":
                self.state.inventory.append(f"Insignia de duelo contra {opponent_name}")

            # Actualizar atributos
            if "valentía" in self.state.attributes:
                self.state.attributes["valentía"] += 1
            else:
                self.state.attributes["valentía"] = 1

            return f"¡Has derrotado a {opponent_name} usando {player_spell}! Tu valentía ha aumentado."
        else:
            return f"{opponent_name} ha bloqueado tu {player_spell}. Necesitas más práctica o un hechizo más poderoso."