# core/achievements.py
class AchievementSystem:
    def __init__(self, game_state):
        self.state = game_state
        self.unlocked = []
        self.achievements = {
            "first_spell": {
                "title": "Primer Hechizo",
                "description": "Lanzaste tu primer hechizo con éxito",
                "reward": "Libro de hechizos básicos"
            },
            "potion_master": {
                "title": "Aprendiz de Pociones",
                "description": "Preparaste tu primera poción correctamente",
                "reward": "Ingrediente raro: Cuerno de unicornio"
            },
            "explorer": {
                "title": "Explorador de Hogwarts",
                "description": "Visitaste 10 ubicaciones diferentes en el castillo",
                "reward": "Mapa detallado de Hogwarts"
            },
            "bookworm": {
                "title": "Ratón de Biblioteca",
                "description": "Pasaste muchas horas estudiando en la Biblioteca",
                "reward": "+2 a Inteligencia"
            },
            "quidditch_fan": {
                "title": "Aficionado al Quidditch",
                "description": "Asististe a tu primer partido de Quidditch",
                "reward": "Bufanda con los colores de tu casa"
            }
        }

    def check_achievement(self, achievement_id):
        """Verifica y desbloquea un logro si no lo tiene ya"""
        if achievement_id not in self.achievements:
            return False

        if achievement_id in self.unlocked:
            return False

        # Desbloquear logro
        self.unlocked.append(achievement_id)
        achievement = self.achievements[achievement_id]

        # Dar recompensa
        reward = achievement["reward"]
        if reward.startswith("+"):
            # Bonus de atributo
            parts = reward.split(" ")
            attr_bonus = int(parts[0].replace("+", ""))
            attr_name = parts[2].lower()

            if attr_name in self.state.attributes:
                self.state.attributes[attr_name] += attr_bonus
            else:
                self.state.attributes[attr_name] = attr_bonus
        else:
            # Item de inventario
            self.state.inventory.append(reward)

        return f"**¡Logro Desbloqueado!**\n\n{achievement['title']}: {achievement['description']}\n\nRecompensa: {reward}"

    def get_achievements(self):
        """Obtiene la lista de logros desbloqueados y disponibles"""
        result = "**Logros Desbloqueados:**\n\n"

        if not self.unlocked:
            result += "Aún no has desbloqueado ningún logro.\n\n"
        else:
            for achievement_id in self.unlocked:
                achievement = self.achievements[achievement_id]
                result += f"✓ {achievement['title']}: {achievement['description']}\n"

            result += "\n"

        result += "**Logros Disponibles:**\n\n"
        for achievement_id, achievement in self.achievements.items():
            if achievement_id not in self.unlocked:
                result += f"□ {achievement['title']}: {achievement['description']}\n"

        return result