import os
import threading
import time
from openai import OpenAI

# Importar módulos del proyecto
from config.settings import MODEL, OPENAI_BASE_URL, OPENAI_API_KEY, SAVES_DIR, AUTOSAVE_INTERVAL
from core.locations import LocationSystem
from core.potions import PotionSystem
from core.quests import QuestSystem
from core.dueling import DuelingSystem
from core.attributes import AttributeSystem
from core.persistence import GameState
from core.characters import CharacterSystem
from core.events import EventSystem
from core.achievements import AchievementSystem
from core.calendar import CalendarSystem

# class HarryPotterGame:
#     def __init__(self):
#         # Inicializar sistemas
#         self.state = GameState(SAVES_DIR)
#         self.attribute_system = AttributeSystem()
#
#         # Cliente de OpenAI
#         self.openai = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
#
#         # Configurar guardado automático
#         self.autosave_thread = None
#         self.running = True
#
#         # Sistema de mensajes
#         self.system_message = """
#         Eres un narrador de historias interactivas en el mundo de Harry Potter.
#         Tu trabajo es guiar al usuario a través de una aventura mágica en Hogwarts,
#         donde tendrá que tomar decisiones que afectarán el desarrollo de la trama.
#         Cada vez que el usuario tome una decisión, debes continuar la historia
#         basándote en esa elección y ofrecer nuevas opciones.
#         El sistema rastreará dinámicamente los atributos del personaje conforme
#         se desarrolle la historia.
#         Asegúrate de que la historia sea coherente, emocionante y fiel al
#         universo de Harry Potter.
#         """
# En app.py, modifica la clase HarryPotterGame

class HarryPotterGame:
    def __init__(self):
        # Inicializar sistemas
        self.state = GameState(SAVES_DIR)
        self.attribute_system = AttributeSystem()

        # Sistemas avanzados
        self.location_system = LocationSystem(self.state)
        self.character_system = CharacterSystem(self.state)
        self.event_system = EventSystem(self.state)
        self.achievement_system = AchievementSystem(self.state)
        self.calendar_system = CalendarSystem(self.state)

        # Diccionario para acceder a los sistemas
        self.systems = {
            "attribute": self.attribute_system,
            "location": self.location_system,
            "character": self.character_system,
            "event": self.event_system,
            "achievement": self.achievement_system,
            "calendar": self.calendar_system
        }

        # Cliente de OpenAI
        self.openai = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

        # Autosave
        self.autosave_thread = None
        self.running = True

        # Sistema de mensajes
        self.system_message = """
        Eres un narrador de historias interactivas en el mundo de Harry Potter.
        Tu trabajo es guiar al usuario a través de una aventura mágica en Hogwarts, 
        donde tendrá que tomar decisiones que afectarán el desarrollo de la trama.

        Sé inmersivo y descriptivo, creando una atmósfera mágica que haga sentir 
        al usuario que realmente está en Hogwarts.

        Responde de manera coherente con el universo de Harry Potter y la ubicación
        actual del jugador.

        Ofrece siempre entre 2-4 opciones claras para continuar la aventura y
        recuerda las elecciones previas del usuario.
        """

    def get_system(self, system_name):
        """Obtiene un sistema por su nombre"""
        return self.systems.get(system_name, None)

    # Resto de métodos...
    def start_autosave(self):
        """Inicia el guardado automático"""
        if self.autosave_thread is None:
            self.autosave_thread = threading.Thread(target=self._auto_save_loop)
            self.autosave_thread.daemon = True
            self.autosave_thread.start()

    def _auto_save_loop(self):
        """Bucle para guardar automáticamente cada cierto tiempo"""
        while self.running:
            time.sleep(AUTOSAVE_INTERVAL)
            if time.time() - self.state.last_save > AUTOSAVE_INTERVAL:
                self.state.save(slot=0, name="AutoSave")
                print("Juego guardado automáticamente")

    def chat(self, message, history_ui=None):
        """Función principal del chatbot"""
        # Actualizar historial
        if history_ui:
            self.state.history = history_ui

        # Procesar comandos especiales
        if message.startswith('/'):
            return self._process_command(message)

        # Crear mensajes para el modelo
        messages = [{"role": "system", "content": self.system_message}]
        messages.extend(self.state.history)
        messages.append({"role": "user", "content": message})

        # Generar respuesta
        try:
            completion = self.openai.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            response = completion.choices[0].message.content

            # Actualizar atributos
            self.attribute_system.update_attributes(message + " " + response)
            self.state.attributes = self.attribute_system.attributes

            # Verificar consecuencias
            consequences = self.attribute_system.check_consequences()
            if consequences:
                response += "\n\n" + consequences

            # Actualizar historial
            self.state.history.append({"role": "user", "content": message})
            self.state.history.append({"role": "assistant", "content": response})

            # Guardar progreso
            self.state.save(slot=0, name="LastSession")

            # Devolver en formato de Gradio (mensaje del usuario y respuesta del asistente)
            return [message, response]

        except Exception as e:
            error_msg = f"Error al comunicarse con el modelo: {str(e)}"
            print(error_msg)
            return [message, error_msg]

    def _process_command(self, command):
        """Procesa comandos especiales"""
        cmd = command.lower().split()

        if cmd[0] == '/inventario':
            response = self._show_inventory()
            self.state.history.append({"role": "user", "content": command})
            self.state.history.append({"role": "assistant", "content": response})
            self.state.save(slot=0, name="LastSession")
            return [command, response]

        elif cmd[0] == '/atributos':
            response = self._show_attributes()
            self.state.history.append({"role": "user", "content": command})
            self.state.history.append({"role": "assistant", "content": response})
            self.state.save(slot=0, name="LastSession")
            return [command, response]

        elif cmd[0] == '/guardar' and len(cmd) > 1:
            try:
                slot = int(cmd[1])
                name = ' '.join(cmd[2:]) if len(cmd) > 2 else None
                filepath = self.state.save(slot=slot, name=name)
                response = f"Juego guardado en slot {slot}"
                self.state.history.append({"role": "user", "content": command})
                self.state.history.append({"role": "assistant", "content": response})
                return [command, response]
            except ValueError:
                response = "El número de slot debe ser un número entero"
                return [command, response]

        elif cmd[0] == '/cargar' and len(cmd) > 1:
            try:
                slot = int(cmd[1])
                if self.state.load(slot=slot):
                    # Sincronizar atributos
                    self.attribute_system.attributes = self.state.attributes
                    response = f"Juego cargado desde slot {slot}"
                    return [command, response]
                else:
                    response = f"No se encontró un guardado en slot {slot}"
                    return [command, response]
            except ValueError:
                response = "El número de slot debe ser un número entero"
                return [command, response]

        elif cmd[0] == '/ayuda':
            response = """
            Comandos disponibles:
            /inventario - Muestra tu inventario
            /atributos - Muestra tus atributos actuales
            /guardar [slot] [nombre] - Guarda la partida en un slot
            /cargar [slot] - Carga una partida guardada
            /ayuda - Muestra esta ayuda
            """
            self.state.history.append({"role": "user", "content": command})
            self.state.history.append({"role": "assistant", "content": response})
            self.state.save(slot=0, name="LastSession")
            return [command, response]

        else:
            response = "Comando no reconocido. Usa /ayuda para ver la lista de comandos."
            self.state.history.append({"role": "user", "content": command})
            self.state.history.append({"role": "assistant", "content": response})
            self.state.save(slot=0, name="LastSession")
            return [command, response]

    def _show_inventory(self):
        """Muestra el inventario del jugador"""
        if not self.state.inventory:
            return "Tu inventario está vacío."

        items = '\n'.join([f"- {item}" for item in self.state.inventory])
        return f"Inventario:\n{items}"

    def _show_attributes(self):
        """Muestra los atributos del jugador"""
        if not self.state.attributes:
            return "Aún no has desarrollado ningún atributo."

        attributes_list = []
        for attr, value in self.state.attributes.items():
            # Convertir el valor a una representación visual
            bar_length = 10
            position = int((value + 10) / 20 * bar_length)
            bar = "▓" * position + "░" * (bar_length - position)

            attributes_list.append(f"{attr.capitalize()}: {value} [{bar}]")

        return "Atributos:\n" + "\n".join(attributes_list)


# Punto de entrada para pruebas
if __name__ == "__main__":
    game = HarryPotterGame()

    # Test simple
    print("Probando el chatbot...")
    response = game.chat("Hola, me gustaría comenzar mi aventura en Hogwarts")
    print(f"Respuesta: {response}")

# Añadir al final del archivo app.py:

from ui.interface import create_interface
import gradio as gr

if __name__ == "__main__":
    game = HarryPotterGame()
    game.start_autosave()

    # Crear la interfaz
    demo = create_interface(game)

    # Lanzar la aplicación
    # Al final de app.py, ajusta el método launch
    demo.launch()