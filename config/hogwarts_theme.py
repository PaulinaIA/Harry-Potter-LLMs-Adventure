import gradio as gr

# Create a minimal theme that should work with any Gradio version
hogwarts_theme = gr.Theme()

# Define custom CSS for your Harry Potter theme
css = """
@import url('https://fonts.googleapis.com/css2?family=Henny+Penny&display=swap');

/* Mejoras específicas para la interfaz de Harry Potter */
:root {
    --hp-dark-blue: #0a0b1e;
    --hp-gold: #dcb45c;
    --hp-button-blue: #4285f4; /* Color actual del botón "Nueva partida" */
    --hp-button-hover: #3b77db;
    --hp-gray-button: #e2e2e2;
    --hp-gray-button-hover: #d0d0d0;
    --hp-parchment: #f9f3e3;
}

/* Estilo de fondo con textura */
body {
    background-color: var(--hp-dark-blue) !important;
    background-image: url('https://www.transparenttextures.com/patterns/parchment.png') !important;
    background-blend-mode: overlay !important;
    color: #333 !important;
}

/* Título principal con estilo mágico */
.title-container h1 {
    font-family: 'Georgia', serif !important;
    color: var(--hp-gold) !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
    letter-spacing: 1px !important;
    font-size: 2.2rem !important;
}

/* Botón de Nueva partida mejorado */
button.primary {
    background: linear-gradient(to bottom, var(--hp-button-blue), #0e1a40) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    box-shadow: 0 2px 10px rgba(66, 133, 244, 0.3) !important;
    transition: all 0.3s ease !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

button.primary:hover {
    background: linear-gradient(to bottom, #5294ff, var(--hp-button-blue)) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.4) !important;
}

/* Botones secundarios (Ver atributos, Ver inventario, Guardar) */
button.secondary {
    background-color: var(--hp-gray-button) !important;
    color: #444 !important;
    border: none !important;
    border-radius: 6px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    font-weight: 600 !important;
}

button.secondary:hover {
    background-color: var(--hp-gray-button-hover) !important;
    color: #222 !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15) !important;
}

/* Contenedor de la información del personaje */
.character-info-container {
    background-color: var(--hp-parchment) !important;
    border: 1px solid rgba(165, 132, 82, 0.3) !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1) !important;
    padding: 20px !important;
    margin-bottom: 20px !important;
}

/* Chatbot mejorado */
.chatbot-container {
    background-color: var(--hp-parchment) !important;
    border: 1px solid rgba(165, 132, 82, 0.3) !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1) !important;
    padding: 15px !important;
    max-height: 400px !important;
    overflow-y: auto !important;
}

/* Área de texto */
textarea, input[type="text"] {
    background-color: white !important;
    border: 1px solid #ddd !important;
    border-radius: 6px !important;
    padding: 12px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

textarea:focus, input[type="text"]:focus {
    border-color: var(--hp-gold) !important;
    box-shadow: 0 0 0 2px rgba(220, 180, 92, 0.25), inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    outline: none !important;
}

/* Botón de enviar mejorado */
.send-button {
    background: linear-gradient(to bottom, var(--hp-button-blue), #3b77db) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(66, 133, 244, 0.3) !important;
}

.send-button:hover {
    background: linear-gradient(to bottom, #5294ff, var(--hp-button-blue)) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.4) !important;
}

/* Tabs mejorados */
.tab-nav {
    border-bottom: 2px solid rgba(165, 132, 82, 0.3) !important;
    margin-bottom: 20px !important;
}

.tab-nav button {
    color: #0e1a40 !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    transition: all 0.3s ease !important;
}

.tab-nav button:hover, 
.tab-nav button.selected {
    color: var(--hp-button-blue) !important;
    border-bottom-color: var(--hp-button-blue) !important;
}

/* Efecto mágico para elementos interactivos */
.magic-effect {
    position: relative !important;
    overflow: hidden !important;
}

.magic-effect::after {
    content: "" !important;
    position: absolute !important;
    top: -50% !important;
    left: -50% !important;
    width: 200% !important;
    height: 200% !important;
    background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%) !important;
    opacity: 0 !important;
    transition: opacity 0.5s ease !important;
    pointer-events: none !important;
}

.magic-effect:hover::after {
    opacity: 1 !important;
}

/* Estilos específicos para el inventario y slots */
.inventory-slot {
    background-color: rgba(249, 243, 227, 0.5) !important;
    border: 1px solid rgba(165, 132, 82, 0.3) !important;
    border-radius: 4px !important;
    padding: 10px !important;
    transition: all 0.3s ease !important;
}

.inventory-slot:hover {
    background-color: rgba(249, 243, 227, 0.8) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

/* Notificaciones y mensajes */
.notification {
    background-color: rgba(220, 180, 92, 0.1) !important;
    border-left: 4px solid var(--hp-gold) !important;
    color: #333 !important;
    padding: 12px !important;
    margin-bottom: 15px !important;
    border-radius: 0 4px 4px 0 !important;
}

/* Mejoras para la sección de atributos del personaje */
.character-attributes {
    margin: 15px 0;
    font-family: 'Georgia', serif;
}

/* Etiquetas de atributos */
.attribute-label {
    display: inline-block;
    width: 100px;
    font-weight: 600;
    color: #333;
    margin-right: 10px;
}

/* Contenedor de las barras de progreso */
.progress-bar-container {
    display: inline-block;
    width: 150px;
    height: 16px;
    background-color: #f0f0f0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
    margin-right: 10px;
    vertical-align: middle;
}

/* Barras de progreso para diferentes atributos */
.progress-bar {
    height: 100%;
    border-radius: 8px;
}

/* Colores específicos para cada tipo de atributo */
.progress-lealtad {
    background: linear-gradient(90deg, #ffd700, #daa520);
}

.progress-creatividad {
    background: linear-gradient(90deg, #4b0082, #9370db);
}

.progress-valor {
    background: linear-gradient(90deg, #8b0000, #ff6347);
}

.progress-inteligencia {
    background: linear-gradient(90deg, #00008b, #1e90ff);
}

/* Valores numéricos de atributos */
.attribute-value {
    display: inline-block;
    min-width: 30px;
    font-weight: bold;
    color: #333;
}

/* Valores positivos y negativos */
.attribute-positive {
    color: #2e7d32;
}

.attribute-negative {
    color: #c62828;
}

/* Botón de atributos mejorado */
.attribute-button {
    display: block;
    width: 100%;
    padding: 12px;
    text-align: center;
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 8px;
    color: #333;
    font-weight: 600;
    transition: all 0.3s ease;
    margin: 15px 0;
    cursor: pointer;
}

.attribute-button:hover {
    background-color: #e8e8e8;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.harry-potter-title {
    font-family: 'Henny Penny', fantasy, serif;
    text-align: center;
    font-size: 2.5rem;
    background: linear-gradient(45deg, #dcb45c 20%, #f5e3b8 40%, #dcb45c 60%, #f5e3b8 80%);
    background-size: 200% auto;
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-shadow: 0px 2px 4px rgba(0,0,0,0.3);
    margin: 1.5rem 0;
    animation: shine 4s linear infinite;
}

@keyframes shine {
    to {
        background-position: 200% center;
    }
}

"""

# Usage in your interface.py:
# def create_interface():
#     with gr.Blocks(theme=hogwarts_theme, css=css) as demo:
#         ...