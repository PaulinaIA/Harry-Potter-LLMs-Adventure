# core/locations.py
class LocationSystem:
    def __init__(self, game_state):
        self.state = game_state
        self.current_location = "Gran Comedor"
        self.locations = {
            "Gran Comedor": {
                "description": "Un enorme salón con cuatro largas mesas para cada casa y una mesa para profesores. El techo encantado refleja el cielo exterior.",
                "connections": ["Vestíbulo de Entrada", "Escaleras Principales"],
                "characters": ["Dumbledore", "McGonagall", "Estudiantes"]
            },
            "Vestíbulo de Entrada": {
                "description": "La entrada principal al castillo. Un amplio espacio con suelos de piedra y grandes puertas de roble.",
                "connections": ["Gran Comedor", "Escaleras Principales", "Terrenos del Castillo"],
                "characters": ["Filch", "Estudiantes"]
            },
            "Escaleras Principales": {
                "description": "Enormes escaleras de mármol que conectan los diferentes pisos del castillo. Ten cuidado, a veces cambian de dirección.",
                "connections": ["Gran Comedor", "Vestíbulo de Entrada", "Pasillo del Primer Piso",
                                "Pasillo del Segundo Piso"],
                "characters": ["Fantasmas", "Estudiantes"]
            },
            "Pasillo del Primer Piso": {
                "description": "Un largo corredor con diversas aulas. Las antorchas iluminan las paredes de piedra.",
                "connections": ["Escaleras Principales", "Aula de Transformaciones", "Aula de Encantamientos"],
                "characters": ["Estudiantes", "Profesores"]
            },
            "Pasillo del Segundo Piso": {
                "description": "Corredor con ventanas que dan a los terrenos. Hay varias armaduras alineadas a lo largo de la pared.",
                "connections": ["Escaleras Principales", "Biblioteca"],
                "characters": ["Peeves", "Estudiantes"]
            },
            "Biblioteca": {
                "description": "Inmensas estanterías llenas de libros mágicos. La sección prohibida está al fondo con una cadena.",
                "connections": ["Pasillo del Segundo Piso", "Sección Prohibida"],
                "characters": ["Madame Pince", "Estudiantes estudiosos"]
            },
            "Aula de Transformaciones": {
                "description": "Un aula espaciosa con pupitres organizados en filas. En el escritorio del profesor hay varios objetos para practicar transformaciones.",
                "connections": ["Pasillo del Primer Piso"],
                "characters": ["Profesora McGonagall"]
            },
            "Aula de Encantamientos": {
                "description": "Un aula luminosa llena de cojines para practicar encantamientos. Libros de hechizos están apilados en las esquinas.",
                "connections": ["Pasillo del Primer Piso"],
                "characters": ["Profesor Flitwick"]
            },
            "Mazmorras": {
                "description": "Pasillos fríos y húmedos bajo el castillo, iluminados por antorchas verdes.",
                "connections": ["Vestíbulo de Entrada", "Aula de Pociones", "Sala Común de Slytherin"],
                "characters": ["Estudiantes de Slytherin"]
            },
            "Aula de Pociones": {
                "description": "Un aula oscura llena de calderos y estanterías con ingredientes extraños.",
                "connections": ["Mazmorras"],
                "characters": ["Profesor Snape"]
            },
            "Terrenos del Castillo": {
                "description": "Amplios jardines verdes que rodean el castillo. A lo lejos se ve el lago negro y el Bosque Prohibido.",
                "connections": ["Vestíbulo de Entrada", "Cabaña de Hagrid", "Campo de Quidditch", "Invernaderos"],
                "characters": ["Estudiantes", "Hagrid"]
            },
            "Cabaña de Hagrid": {
                "description": "Una pequeña pero acogedora cabaña de piedra con techo de paja. Hay diversos artefactos y plantas extrañas alrededor.",
                "connections": ["Terrenos del Castillo", "Bosque Prohibido"],
                "characters": ["Hagrid", "Fang"]
            },
            "Bosque Prohibido": {
                "description": "Un bosque oscuro y denso con árboles enormes. Los ruidos misteriosos hacen que te mantengas alerta.",
                "connections": ["Cabaña de Hagrid"],
                "characters": ["Criaturas mágicas"],
                "restricted": True
            },
            "Campo de Quidditch": {
                "description": "Un gran estadio con altos postes dorados. Las gradas están decoradas con los colores de las casas.",
                "connections": ["Terrenos del Castillo"],
                "characters": ["Equipos de Quidditch", "Madame Hooch"]
            },
            "Invernaderos": {
                "description": "Varias estructuras de cristal llenas de plantas mágicas exóticas y potencialmente peligrosas.",
                "connections": ["Terrenos del Castillo"],
                "characters": ["Profesora Sprout", "Estudiantes de Herbología"]
            }
        }

    def move_to(self, location):
        """Mueve al jugador a una nueva ubicación"""
        # Normalizar formato (primera letra mayúscula para cada palabra)
        location = ' '.join(word.capitalize() for word in location.split())

        # Verificar si la ubicación existe
        if location not in self.locations:
            return f"No puedes ir a '{location}'. No existe ese lugar en Hogwarts."

        # Verificar si hay conexión desde la ubicación actual
        if location not in self.locations[self.current_location]["connections"]:
            return f"No puedes ir directamente de {self.current_location} a {location}. Debes encontrar un camino."

        # Verificar restricciones
        if self.locations[location].get("restricted", False):
            return f"No puedes entrar a {location}. Esta área está restringida o prohibida."

        # Mover al personaje
        self.current_location = location

        # Obtener descripción y personajes
        description = self.locations[location]["description"]
        characters = ", ".join(self.locations[location]["characters"])
        connections = ", ".join(self.locations[location]["connections"])

        return f"Te has movido a: {location}\n\n{description}\n\nPersonajes presentes: {characters}\n\nDesde aquí puedes ir a: {connections}"

    def get_current_location_info(self):
        """Obtiene información de la ubicación actual"""
        location = self.current_location
        desc = self.locations[location]["description"]
        characters = ", ".join(self.locations[location]["characters"])
        connections = ", ".join(self.locations[location]["connections"])

        return f"**Ubicación actual: {location}**\n\n{desc}\n\nPersonajes presentes: {characters}\n\nPuedes ir a: {connections}"