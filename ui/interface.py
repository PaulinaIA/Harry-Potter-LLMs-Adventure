import os
import gradio as gr
import time
from core.attributes import AttributeSystem
from config.hogwarts_theme import hogwarts_theme, css

# Intenta importar MODEL, pero proporciona un valor predeterminado si falla
try:
    from config.settings import MODEL

    model_name = MODEL
except ImportError:
    model_name = "deepseek-coder:latest"


def create_interface(game):
    """Crea la interfaz optimizada del juego con Gradio"""

    def submit_fn(message, history):
        """Función para mostrar inmediatamente el mensaje del usuario"""
        if not message.strip():
            return history, ""
        # Añade el mensaje del usuario inmediatamente y limpia el input
        return history + [[message, None]], ""

    def process_message(history):
        """Procesa el último mensaje en el historial y genera una respuesta"""
        if not history or len(history[-1]) < 2 or history[-1][1] is not None:
            # No hay mensaje nuevo para procesar
            return history

        user_message = history[-1][0]

        try:
            # Crear historial para el modelo
            history_dict = []
            for i in range(len(history) - 1):  # Excluir el último mensaje sin respuesta
                if history[i][0] and history[i][1]:
                    history_dict.append({"role": "user", "content": history[i][0]})
                    history_dict.append({"role": "assistant", "content": history[i][1]})

            # Comandos especiales
            if user_message.startswith('/'):
                cmd = user_message.lower().split()
                if cmd[0] == '/inventario':
                    response = game._show_inventory()
                elif cmd[0] == '/atributos':
                    response = game._show_attributes()
                elif cmd[0] == '/ayuda':
                    response = """
                    Comandos disponibles:
                    /inventario - Muestra tu inventario
                    /atributos - Muestra tus atributos actuales
                    /guardar [slot] [nombre] - Guarda la partida en un slot
                    /cargar [slot] - Carga una partida guardada
                    /ayuda - Muestra esta ayuda
                    """
                # Añadir estos comandos en la función process_message

                elif cmd[0] == '/ubicacion':
                    location_system = game.get_system("location")
                    if location_system:
                        if len(cmd) > 1:
                            location = " ".join(cmd[1:])
                            response = location_system.move_to(location)
                        else:
                            response = location_system.get_current_location_info()
                    else:
                        response = "El sistema de ubicaciones no está disponible."

                elif cmd[0] == '/duelo':
                    if len(cmd) > 1:
                        spell = " ".join(cmd[1:])
                        dueling_system = game.get_system("dueling")
                        response = dueling_system.duel(spell)
                    else:
                        response = "Debes especificar un hechizo para el duelo. Ejemplo: /duelo expelliarmus"

                elif cmd[0] == '/pocion':
                    if len(cmd) > 1:
                        ingredients = " ".join(cmd[1:]).split(",")
                        ingredients = [i.strip() for i in ingredients]
                        potion_system = game.get_system("potion")
                        response = potion_system.brew_potion(ingredients)
                    else:
                        response = "Debes especificar los ingredientes separados por comas. Ejemplo: /pocion ajenjo, díctamo"

                elif cmd[0] == '/misiones':
                    quest_system = game.get_system("quest")
                    response = quest_system.get_active_quests()

                elif cmd[0] == '/aceptar':
                    if len(cmd) > 1:
                        quest_id = cmd[1]
                        quest_system = game.get_system("quest")
                        response = quest_system.start_quest(quest_id)
                    else:
                        response = "Debes especificar el ID de la misión. Ejemplo: /aceptar intro_library"

                elif cmd[0] == '/completar':
                    if len(cmd) > 1:
                        quest_id = cmd[1]
                        quest_system = game.get_system("quest")
                        response = quest_system.complete_quest(quest_id)
                    else:
                        response = "Debes especificar el ID de la misión. Ejemplo: /completar intro_library"
                elif cmd[0] == '/guardar' and len(cmd) > 1:
                    try:
                        slot = int(cmd[1])
                        name = ' '.join(cmd[2:]) if len(cmd) > 2 else None
                        game.state.save(slot=slot, name=name)
                        response = f"Juego guardado en slot {slot}"
                    except ValueError:
                        response = "El número de slot debe ser un número entero"
                elif cmd[0] == '/cargar' and len(cmd) > 1:
                    try:
                        slot = int(cmd[1])
                        if game.state.load(slot=slot):
                            game.attribute_system.attributes = game.state.attributes
                            response = f"Juego cargado desde slot {slot}"
                        else:
                            response = f"No se encontró un guardado en slot {slot}"
                    except ValueError:
                        response = "El número de slot debe ser un número entero"
                else:
                    response = "Comando no reconocido. Usa /ayuda para ver la lista de comandos."
            else:
                # Mensaje normal para el chatbot
                # Crear mensajes para el modelo
                messages = [{"role": "system", "content": game.system_message}]
                messages.extend(history_dict)
                messages.append({"role": "user", "content": user_message})

                # Generar respuesta del modelo
                completion = game.openai.chat.completions.create(
                    model=model_name,
                    messages=messages
                )
                response = completion.choices[0].message.content

                # Actualizar atributos
                game.attribute_system.update_attributes(user_message + " " + response)
                game.state.attributes = game.attribute_system.attributes

                # Verificar consecuencias
                consequences = game.attribute_system.check_consequences()
                if consequences:
                    response += "\n\n" + consequences

            # Actualizar historial interno
            game.state.history.append({"role": "user", "content": user_message})
            game.state.history.append({"role": "assistant", "content": response})

            # Guardar progreso
            game.state.save(slot=0, name="LastSession")

            # Actualizar la última respuesta
            history[-1][1] = response
            return history

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            history[-1][1] = error_msg
            return history

    def show_attributes():
        """Muestra los atributos actuales"""
        return game._show_attributes()

    def show_inventory():
        """Muestra el inventario actual"""
        return game._show_inventory()

    def start_new_game():
        """Inicia una nueva partida"""
        try:
            # Reiniciar el estado del juego
            game.state = type(game.state)(game.state.saves_dir)
            game.attribute_system = AttributeSystem()
            game.state.history = []

            # Mensaje inicial
            message = "¡Comienza tu nueva aventura en Hogwarts! Dime tu nombre y qué casa prefieres."

            # Actualizar historial del juego
            game.state.history.append({"role": "assistant", "content": message})

            # Devolver un historial limpio con solo el mensaje inicial
            return [[None, message]]
        except Exception as e:
            print(f"Error al iniciar nueva partida: {e}")
            return [[None, f"Error al iniciar nueva partida: {e}"]]

    def save_game(slot, name):
        """Guarda la partida en un slot específico"""
        if not slot.isdigit():
            return "El número de slot debe ser un número entero"

        slot_num = int(slot)
        filepath = game.state.save(slot=slot_num, name=name if name else None)
        return f"Juego guardado en slot {slot_num}"

    def load_game(slot):
        """Carga una partida guardada"""
        if not slot.isdigit():
            return "El número de slot debe ser un número entero"

        slot_num = int(slot)
        if game.state.load(slot=slot_num):
            game.attribute_system.attributes = game.state.attributes
            return f"Juego cargado desde slot {slot_num}"
        else:
            return f"No se encontró un guardado en slot {slot_num}"

    def list_saves():
        """Lista todas las partidas guardadas"""
        saves = game.state.get_save_slots()
        if not saves:
            return "No hay partidas guardadas."

        saves_list = []
        for save in saves:
            timestamp = time.strftime("%d/%m/%Y %H:%M", time.localtime(save["timestamp"]))
            saves_list.append(f"Slot {save['slot']}: {save['name']} - {timestamp}")

        return "Partidas guardadas:\n" + "\n".join(saves_list)

    # def move_location(location):
    #     """Función para moverse a una ubicación en el mapa"""
    #     try:
    #         # Intentar obtener el sistema de ubicaciones
    #         location_system = game.get_system("location")
    #         if not location_system:
    #             return "Sistema de ubicaciones no disponible.", current_location.value, available_locations.value
    #
    #         # Intentar moverse
    #         result = location_system.move_to(location)
    #         current = location_system.current_location
    #
    #         # Obtener conexiones disponibles
    #         connections = ", ".join(location_system.locations[current]["connections"])
    #
    #         return result, f"**Ubicación actual:** {current}", f"**Lugares disponibles desde aquí:**\n{connections}"
    #     except Exception as e:
    #         return f"Error al mover: {str(e)}", current_location.value, available_locations.value

    # Añadir esta función en interface.py
    def update_location_image():
        """Actualiza la imagen según la ubicación actual"""
        location_system = game.get_system("location")
        if not location_system:
            return "assets/images/hogwarts_default.jpg"

        location = location_system.current_location
        location_filename = location.lower().replace(' ', '_') + ".jpg"

        # Rutas de imágenes
        location_path = os.path.join("assets", "images", "locations", location_filename)
        default_path = os.path.join("assets", "images", "hogwarts_default.jpg")

        # Verificar si existe la imagen específica
        if os.path.exists(location_path):
            return location_path
        else:
            return default_path

    # with gr.Blocks(title="Aventura en Hogwarts", theme=hogwarts_theme) as demo:
    #     # Banner de título con imagen
    #     with gr.Row():
    #         gr.HTML("""
    #         <div style="text-align: center; margin-bottom: 10px; width: 100%;">
    #             <img src="https://i.imgur.com/YourHogwartsBanner.png" style="max-width: 80%; height: auto;">
    #             <h1 style="font-family: 'Garamond', serif; color: #3c096c; margin-top: 0; font-size: 2.5em;">
    #                 Aventura en el Mundo de Harry Potter
    #             </h1>
    #         </div>
    #         """)
    #with gr.Blocks(title="Aventura en Hogwarts", theme=gr.themes.Soft()) as demo:
    with gr.Blocks(title="Aventura en Hogwarts", theme=hogwarts_theme, css=css) as demo:
        gr.HTML('<h1 class="harry-potter-title">Aventura en el Mundo de Harry Potter</h1>')

        with gr.Tabs() as tabs:
            with gr.TabItem("Aventura Principal"):
                with gr.Row():
                    with gr.Column(scale=1):
                        # Panel lateral (mantén el mismo contenido que tenías)
                        with gr.Column():
                             gr.Markdown("### Información del personaje")
                             attributes_display = gr.Markdown("Cargando atributos...")
                             attributes_button = gr.Button("Ver atributos", variant="secondary")

                        # with gr.Column():
                        #      gr.Markdown("### Inventario")
                        #      inventory_display = gr.Markdown("Cargando inventario...")
                        #      inventory_button = gr.Button("Ver inventario", variant="secondary")

                        with gr.Column():
                            gr.Markdown("### Gestión de partidas")
                            with gr.Row():
                                new_game_button = gr.Button("Nueva partida", variant="primary")

                            with gr.Row():
                                save_slot = gr.Textbox(label="Slot", value="1")
                                save_name = gr.Textbox(label="Nombre", placeholder="Mi aventura")

                            with gr.Row():
                                save_button = gr.Button("Guardar", variant="secondary")
                                load_button = gr.Button("Cargar", variant="secondary")

                            saves_display = gr.Markdown("No hay partidas guardadas")
                            list_saves_button = gr.Button("Listar partidas", variant="secondary")

                    with gr.Column(scale=2):
                        # Chat principal (mantén el mismo contenido que tenías)
                        chatbot = gr.Chatbot(
                            height=500,
                            show_copy_button=True,
                            elem_id="harry-potter-chat"
                        )

                        with gr.Row():
                            # message = gr.Textbox(
                            #     placeholder="¿Qué quieres hacer?",
                            #     lines=2,
                            #     interactive=True,
                            #     elem_id="user-message-input",
                            #     submit=True
                            # )
                            # submit_button = gr.Button("Enviar", variant="primary")
                            message = gr.Textbox(
                                placeholder="¿Qué quieres hacer?",
                                lines=1,
                                interactive=True,
                                elem_id="user-message-input"
                            )
                            submit_button = gr.Button("Enviar", variant="primary", scale=0.3)
                        # Información de comandos
                        gr.Markdown("""
                        ### Comandos disponibles:
                        - `/atributos` - Muestra tus atributos actuales
                        - `/guardar [slot] [nombre]` - Guarda la partida en un slot
                        - `/cargar [slot]` - Carga una partida guardada
                        - `/ayuda` - Muestra ayuda adicional
                        """)
            #- `/inventario` - Muestra tu inventario
            #- `/ubicacion [lugar]` - Ver o moverte a una ubicación
            #- `/duelo [hechizo]` - Iniciar un duelo con un hechizo
            #- `/pocion [ingredientes]` - Preparar una poción
            #- `/misiones` - Ver misiones activas
            # AQUÍ VA LA NUEVA PESTAÑA DE MAPA
            # with gr.TabItem("Mapa de Hogwarts"):
            #     gr.Markdown("### Explora Hogwarts")
            #
            #     # Cargar imagen del mapa (puedes reemplazar esto con una URL real)
            #     hogwarts_map = gr.Image(value="assets/images/hogwarts_map.jpg", label="Mapa de Hogwarts") #.scale(height=400)
            #
            #     with gr.Row():
            #         current_location = gr.Markdown("**Ubicación actual:** Gran Comedor")
            #
            #     with gr.Row():
            #         location_input = gr.Textbox(
            #             label="¿A dónde quieres ir?",
            #             placeholder="Ej: Biblioteca, Mazmorras, etc."
            #         )
            #         move_button = gr.Button("Ir", variant="primary")
            #
            #     available_locations = gr.Markdown(
            #         "**Lugares disponibles desde aquí:**\nVestíbulo de Entrada, Escaleras Principales")
            # with gr.TabItem("Personajes y Calendario"):
            #     with gr.Row():
            #         with gr.Column():
            #             gr.Markdown("### Calendario y Horario")
            #             calendar_info = gr.Markdown("Cargando información de tiempo...")
            #             advance_time_button = gr.Button("Avanzar tiempo", variant="secondary")
            #
            #         with gr.Column():
            #             gr.Markdown("### Hablar con Personajes")
            #             character_input = gr.Textbox(
            #                 label="¿Con quién quieres hablar?",
            #                 placeholder="Ej: Dumbledore, McGonagall, Snape"
            #             )
            #             talk_button = gr.Button("Hablar", variant="primary")
            #             character_response = gr.Markdown("Selecciona un personaje para hablar con él.")

        def send_message(message, history):
            if not message.strip():
                return history, ""

            # Agregar mensaje del usuario
            new_history = history + [[message, None]]

            # Nota: Devolvemos el mensaje vacío para limpiar el input
            return new_history, ""

        def process_response(history):
            # Solo procesa si hay un mensaje pendiente (sin respuesta)
            if not history or history[-1][1] is not None:
                return history

            try:
                # Usar la función existente pero asegurarnos de capturar excepciones
                return process_message(history)
            except Exception as e:
                print(f"Error procesando respuesta: {e}")
                # En caso de error, agregar un mensaje de error como respuesta
                history[-1][1] = f"Error: No se pudo procesar tu mensaje. {str(e)}"
                return history

        # Configurar los eventos para el botón de envío y la tecla Enter
        submit_button.click(
            fn=send_message,
            inputs=[message, chatbot],
            outputs=[chatbot, message],
            queue=False
        ).then(
            fn=process_response,
            inputs=chatbot,
            outputs=chatbot
        )

        message.submit(
            fn=send_message,
            inputs=[message, chatbot],
            outputs=[chatbot, message],
            queue=False
        ).then(
            fn=process_response,
            inputs=chatbot,
            outputs=chatbot
        )
        # Limpieza de chatbot al iniciar nueva partida
        new_game_button.click(lambda: None, None, chatbot, js="(x) => []")
        new_game_button.click(start_new_game, outputs=chatbot)

        # Resto de eventos
        attributes_button.click(show_attributes, outputs=attributes_display)
        #inventory_button.click(show_inventory, outputs=inventory_display)

        #move_button.click(move_location,inputs=[location_input],outputs=[gr.Markdown("resultado_movimiento", visible=False), current_location, available_locations])
        save_button.click(save_game, inputs=[save_slot, save_name], outputs=saves_display)
        load_button.click(load_game, inputs=[save_slot], outputs=saves_display)
        list_saves_button.click(list_saves, outputs=saves_display)

        # # Eventos para personajes y calendario
        # advance_time_button.click(
        #     lambda: game.get_system("calendar").advance_time() if game.get_system(
        #         "calendar") else "Sistema de calendario no disponible.",
        #     None,
        #     calendar_info
        # )
        #
        # talk_button.click(
        #     lambda character: game.get_system("character").talk_to(character) if game.get_system(
        #         "character") else "Sistema de personajes no disponible.",
        #     inputs=[character_input],
        #     outputs=[character_response]
        # )

        # # Actualizar calendario al cargar
        # demo.load(
        #     lambda: game.get_system("calendar").get_current_time_info() if game.get_system(
        #         "calendar") else "Calendario no disponible.",
        #     None,
        #     calendar_info
        # )
        # Actualizar información al cargar
        demo.load(show_attributes, outputs=attributes_display)
        #demo.load(show_inventory, outputs=inventory_display)
        demo.load(list_saves, outputs=saves_display)

    return demo