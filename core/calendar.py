# core/calendar.py
from datetime import datetime, timedelta
class CalendarSystem:
    def __init__(self, game_state):
        self.state = game_state

        # Fechas del año escolar
        self.year = 1991  # Primer libro de Harry Potter
        self.start_date = datetime(self.year, 9, 1)  # 1 de septiembre
        self.current_date = self.start_date
        self.end_date = datetime(self.year + 1, 6, 30)  # 30 de junio

        # Períodos del día
        self.periods = ["Mañana", "Mediodía", "Tarde", "Noche", "Madrugada"]
        self.current_period = 0  # Mañana

        # Eventos especiales del calendario
        self.special_events = {
            (10, 31): "Fiesta de Halloween",
            (12, 25): "Navidad",
            (12, 31): "Año Nuevo",
            (2, 14): "Día de San Valentín",
            (self.year + 1, 6, 30): "Banquete de Fin de Curso"
        }

        # Horario de clases según el día
        self.weekday_classes = {
            0: {  # Lunes
                "Mañana": "Transformaciones",
                "Mediodía": "Almuerzo",
                "Tarde": "Pociones"
            },
            1: {  # Martes
                "Mañana": "Encantamientos",
                "Mediodía": "Almuerzo",
                "Tarde": "Historia de la Magia"
            },
            2: {  # Miércoles
                "Mañana": "Herbología",
                "Mediodía": "Almuerzo",
                "Tarde": "Defensa Contra las Artes Oscuras"
            },
            3: {  # Jueves
                "Mañana": "Transformaciones",
                "Mediodía": "Almuerzo",
                "Tarde": "Astronomía"
            },
            4: {  # Viernes
                "Mañana": "Pociones doble",
                "Mediodía": "Almuerzo",
                "Tarde": "Libre"
            },
            5: {  # Sábado
                "Mañana": "Libre",
                "Mediodía": "Almuerzo",
                "Tarde": "Libre"
            },
            6: {  # Domingo
                "Mañana": "Libre",
                "Mediodía": "Almuerzo",
                "Tarde": "Libre"
            }
        }

    def advance_time(self, periods=1):
        """Avanza el tiempo en períodos"""
        for _ in range(periods):
            self.current_period = (self.current_period + 1) % len(self.periods)

            # Si llegamos a la madrugada, avanzamos un día
            if self.current_period == 4:  # Madrugada
                self.current_date += timedelta(days=1)

        return self.get_current_time_info()

    def get_current_time_info(self):
        """Obtiene información sobre la fecha y hora actuales"""
        day_str = self.current_date.strftime("%A, %d de %B de %Y")
        period_str = self.periods[self.current_period]

        result = f"**{day_str}, {period_str}**\n\n"

        # Verificar eventos especiales
        event_key = (self.current_date.month, self.current_date.day)
        special_event = self.special_events.get(event_key, None)

        if special_event:
            result += f"¡Hoy es {special_event}!\n\n"

        # Verificar horario de clases
        weekday = self.current_date.weekday()
        class_schedule = self.weekday_classes.get(weekday, {})
        current_class = class_schedule.get(period_str, "Tiempo libre")

        if current_class != "Libre" and current_class != "Almuerzo":
            result += f"En este momento tienes clase de: {current_class}\n"
        elif current_class == "Almuerzo":
            result += "Es hora de almorzar en el Gran Comedor.\n"
        else:
            result += "Tienes tiempo libre para explorar o estudiar.\n"

        return result