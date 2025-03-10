# core/characters.py
class CharacterSystem:
    def __init__(self, game_state):
        self.state = game_state
        self.relationships = {}  # Nivel de relación con cada personaje (-10 a 10)
        self.characters = {
            "Albus Dumbledore": {
                "title": "Director",
                "house": None,
                "description": "El sabio y poderoso director de Hogwarts.",
                "dialog": {
                    "greeting": "Ah, {name}. Las decisiones que tomamos muestran lo que somos, mucho más que nuestras habilidades.",
                    "friendly": "Siempre es un placer conversar con un estudiante tan brillante.",
                    "neutral": "¿Hay algo específico que necesites discutir?",
                    "unfriendly": "Espero que estés utilizando tu tiempo en Hogwarts sabiamente."
                }
            },
            "Minerva McGonagall": {
                "title": "Profesora de Transformaciones",
                "house": "Gryffindor",
                "description": "Estricta pero justa, la subdirectora de Hogwarts.",
                "dialog": {
                    "greeting": "Bienvenido/a a clase, {name}.",
                    "friendly": "Su progreso en Transformaciones es notable, {name}.",
                    "neutral": "Espero que esté practicando adecuadamente.",
                    "unfriendly": "La disciplina es crucial para dominar la Transformación."
                }
            },
            "Severus Snape": {
                "title": "Profesor de Pociones",
                "house": "Slytherin",
                "description": "El sombrío y severo maestro de pociones.",
                "dialog": {
                    "greeting": "{name}... espero que esté preparado/a para la clase de hoy.",
                    "friendly": "Su poción es... aceptable.",
                    "neutral": "No toleraré errores en mi clase.",
                    "unfriendly": "Claramente la fama no lo es todo, ¿verdad, {name}?"
                }
            },
            "Rubeus Hagrid": {
                "title": "Guardián de las Llaves y Terrenos",
                "house": "Gryffindor",
                "description": "El amable semigigante con pasión por las criaturas mágicas.",
                "dialog": {
                    "greeting": "¡{name}! ¡Qué alegría verte!",
                    "friendly": "Pasa y toma un té. Tengo galletas recién horneadas.",
                    "neutral": "¿Vienes a visitar? Estaba alimentando a las criaturas.",
                    "unfriendly": "No te había visto en mucho tiempo..."
                }
            }
        }

    def talk_to(self, character_name):
        """Iniciar conversación con un personaje"""
        # Normalizar formato
        character_name = ' '.join(word.capitalize() for word in character_name.split())

        # Verificar si el personaje existe
        if character_name not in self.characters:
            return f"No encuentras a {character_name} por aquí."

        # Verificar si el personaje está en la ubicación actual
        location_system = self.state.get_system("location")
        if location_system:
            current_location = location_system.current_location
            characters_here = location_system.locations[current_location]["characters"]

            if character_name not in characters_here:
                return f"{character_name} no está en {current_location} en este momento."

        # Obtener nivel de relación
        relation = self.relationships.get(character_name, 0)

        # Determinar tipo de diálogo según relación
        dialog_type = "greeting"
        if relation > 3:
            dialog_type = "friendly"
        elif relation < -3:
            dialog_type = "unfriendly"
        elif relation != 0:
            dialog_type = "neutral"

        # Obtener el diálogo
        character = self.characters[character_name]
        dialog = character["dialog"][dialog_type]

        # Formatear con el nombre del jugador
        player_name = self.state.character_name or "estudiante"
        dialog = dialog.format(name=player_name)

        # Construir respuesta
        response = f"**{character_name}, {character['title']}**\n\n"
        response += f"{character['description']}\n\n"
        response += f'"{dialog}"'

        return response

    def change_relationship(self, character_name, amount):
        """Cambia la relación con un personaje"""
        if character_name in self.characters:
            current = self.relationships.get(character_name, 0)
            self.relationships[character_name] = max(-10, min(10, current + amount))
            return True
        return False