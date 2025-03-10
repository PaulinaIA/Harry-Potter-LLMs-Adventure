# core/quests.py
class QuestSystem:
    def __init__(self, game_state):
        self.state = game_state
        self.active_quests = []
        self.completed_quests = []
        self.available_quests = [
            {
                "id": "intro_library",
                "title": "El libro perdido",
                "description": "Madame Pince necesita encontrar un libro especial sobre pociones que ha desaparecido de la biblioteca.",
                "location": "Biblioteca",
                "objective": "Buscar en el Aula de Pociones",
                "reward": "10 puntos para tu casa y un libro de hechizos básicos",
                "prerequisite": None
            },
            {
                "id": "herbology_help",
                "title": "Plantas problemáticas",
                "description": "La profesora Sprout necesita ayuda para recolectar ingredientes para la clase de Herbología.",
                "location": "Invernaderos",
                "objective": "Recolectar 3 plantas mágicas",
                "reward": "Raíz de mandrágora para pociones",
                "prerequisite": None
            },
            {
                "id": "ghost_message",
                "title": "Mensaje fantasmal",
                "description": "Nick Casi Decapitado necesita que entregues un mensaje a la Dama Gris.",
                "location": "Pasillo del Segundo Piso",
                "objective": "Hablar con la Dama Gris en la Torre de Ravenclaw",
                "reward": "Información sobre la historia secreta de Hogwarts",
                "prerequisite": "intro_library"
            }
        ]

    def get_available_quests(self):
        """Obtiene misiones disponibles según la ubicación y prerrequisitos"""
        location_system = self.state.get_system("location")
        current_location = location_system.current_location

        available = []
        for quest in self.available_quests:
            # Verificar si ya está activa o completada
            if any(q["id"] == quest["id"] for q in self.active_quests + self.completed_quests):
                continue

            # Verificar ubicación
            if quest["location"] != current_location:
                continue

            # Verificar prerrequisitos
            if quest["prerequisite"] and not any(q["id"] == quest["prerequisite"] for q in self.completed_quests):
                continue

            available.append(quest)

        return available

    def start_quest(self, quest_id):
        """Inicia una misión por su ID"""
        # Buscar la misión en las disponibles
        quest = None
        for q in self.available_quests:
            if q["id"] == quest_id:
                quest = q
                break

        if not quest:
            return f"No hay ninguna misión con ID '{quest_id}' disponible."

        # Añadir a misiones activas
        self.active_quests.append(quest)

        return f"Has comenzado la misión: {quest['title']}\n\n{quest['description']}\n\nObjetivo: {quest['objective']}"

    def complete_quest(self, quest_id):
        """Completa una misión activa"""
        # Buscar la misión en las activas
        quest = None
        for i, q in enumerate(self.active_quests):
            if q["id"] == quest_id:
                quest = q
                del self.active_quests[i]
                break

        if not quest:
            return f"No tienes ninguna misión activa con ID '{quest_id}'."

        # Añadir a misiones completadas
        self.completed_quests.append(quest)

        # Dar recompensa
        if "puntos" in quest["reward"].lower():
            # Agregar puntos a la casa
            points = int(''.join(filter(str.isdigit, quest["reward"])))
            # TODO: implementar sistema de puntos de casa

        if "ingrediente" in quest["reward"].lower() or "poción" in quest["reward"].lower():
            # Agregar item al inventario
            reward_item = quest["reward"].split("y ")[-1] if "y " in quest["reward"] else quest["reward"]
            self.state.inventory.append(reward_item)

        return f"¡Has completado la misión: {quest['title']}!\n\nRecompensa: {quest['reward']}"

    def get_active_quests(self):
        """Obtiene listado de misiones activas"""
        if not self.active_quests:
            return "No tienes misiones activas actualmente."

        result = "**Misiones activas:**\n\n"
        for quest in self.active_quests:
            result += f"• {quest['title']}: {quest['objective']}\n"

        return result