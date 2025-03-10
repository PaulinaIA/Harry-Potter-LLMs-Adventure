# core/events.py
import random


class EventSystem:
    def __init__(self, game_state):
        self.state = game_state
        self.last_event_time = 0
        self.events = {
            "Gran Comedor": [
                {
                    "title": "Carta Inesperada",
                    "description": "Una lechuza deja caer una carta frente a ti. Es de tu familia.",
                    "choices": ["Abrirla ahora", "Guardarla para más tarde", "Compartirla con amigos"],
                    "outcomes": [
                        "La carta contiene noticias de casa y un pequeño regalo.",
                        "Guardas la carta en tu bolsillo para leerla después.",
                        "Tus amigos se interesan por las noticias de tu familia."
                    ]
                },
                {
                    "title": "Anuncio de Dumbledore",
                    "description": "Dumbledore se levanta para hacer un anuncio importante.",
                    "choices": ["Escuchar atentamente", "Seguir comiendo", "Comentar con tus compañeros"],
                    "outcomes": [
                        "Te enteras de que habrá un torneo de duelos entre casas.",
                        "Te pierdes parte del anuncio por estar distraído.",
                        "Tus compañeros están emocionados por la noticia."
                    ]
                }
            ],
            "Biblioteca": [
                {
                    "title": "Libro Susurrante",
                    "description": "Escuchas susurros que provienen de un libro en un estante cercano.",
                    "choices": ["Investigar el libro", "Ignorarlo", "Informar a Madame Pince"],
                    "outcomes": [
                        "Descubres un antiguo libro de hechizos con notas en los márgenes.",
                        "Los susurros cesan después de un rato.",
                        "Madame Pince revisa el libro y lo coloca en la Sección Prohibida."
                    ]
                }
            ],
            "Pasillo del Tercer Piso": [
                {
                    "title": "Peeves",
                    "description": "Peeves el poltergeist está causando problemas en el pasillo.",
                    "choices": ["Evitarlo", "Enfrentarlo", "Buscar ayuda"],
                    "outcomes": [
                        "Logras pasar sin que te note.",
                        "Peeves te molesta pero eventualmente se aburre y se va.",
                        "El Barón Sanguinario aparece y ahuyenta a Peeves."
                    ]
                }
            ]
        }

    def check_for_random_event(self):
        """Verifica si debe ocurrir un evento aleatorio"""
        # Obtener ubicación actual
        location_system = self.state.get_system("location")
        if not location_system:
            return None

        current_location = location_system.current_location

        # Verificar si hay eventos para esta ubicación
        if current_location not in self.events:
            return None

        # Probabilidad de evento (20%)
        if random.random() > 0.2:
            return None

        # Seleccionar evento aleatorio
        event = random.choice(self.events[current_location])

        return self.format_event(event)

    def format_event(self, event):
        """Formatea un evento para presentarlo"""
        result = f"**{event['title']}**\n\n"
        result += f"{event['description']}\n\n"
        result += "¿Qué haces?\n\n"

        for i, choice in enumerate(event['choices']):
            result += f"{i + 1}. {choice}\n"

        # Guardar evento actual para procesar elección
        self.current_event = event

        return result

    def process_event_choice(self, choice_index):
        """Procesa la elección del jugador para un evento"""
        if not hasattr(self, 'current_event'):
            return "No hay un evento activo para responder."

        # Validar índice
        if choice_index < 0 or choice_index >= len(self.current_event['outcomes']):
            return "Esa no es una opción válida."

        outcome = self.current_event['outcomes'][choice_index]

        # Limpiar evento actual
        del self.current_event

        return outcome