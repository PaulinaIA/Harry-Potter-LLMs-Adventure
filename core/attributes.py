class AttributeSystem:
    def __init__(self):
        self.attributes = {}
        self.attribute_keywords = {
            "valentía": {
                "positive": ["valiente", "valor", "coraje", "enfrentar", "heroico"],
                "negative": ["cobarde", "miedo", "huir", "esconderse"]
            },
            "astucia": {
                "positive": ["astuto", "astucia", "engaño", "estrategia", "ingenioso"],
                "negative": ["ingenuo", "crédulo", "descuidado", "imprudente"]
            },
            "inteligencia": {
                "positive": ["inteligente", "sabio", "conocimiento", "sabiduría", "lógica", "estudiar"],
                "negative": ["ignorante", "olvidadizo", "distraído", "confundido"]
            },
            "lealtad": {
                "positive": ["leal", "fiel", "amistad", "compañerismo", "confianza", "honesto"],
                "negative": ["traidor", "desleal", "egoísta", "mentiroso"]
            },
            "creatividad": {
                "positive": ["creativo", "artístico", "imaginativo", "innovador", "original"],
                "negative": ["rígido", "inflexible", "convencional", "predecible"]
            }
        }

    def update_attributes(self, text):
        """Actualiza los atributos basados en el texto"""
        detected = self._detect_attributes(text.lower())

        # Actualizar atributos existentes o crear nuevos
        for attr, value in detected.items():
            if attr in self.attributes:
                self.attributes[attr] += value
            else:
                self.attributes[attr] = value

            # Limitar valores a rango -10 a 10
            self.attributes[attr] = max(-10, min(10, self.attributes[attr]))

        return self.attributes

    def _detect_attributes(self, text):
        """Detecta atributos en el texto"""
        detected_attributes = {}

        # Buscar palabras clave
        for attr, keywords in self.attribute_keywords.items():
            score = 0

            # Verificar palabras positivas
            for keyword in keywords["positive"]:
                if keyword in text:
                    # Verificar contexto negativo
                    if f"no {keyword}" in text or f"sin {keyword}" in text:
                        score -= 1
                    else:
                        score += 1

            # Verificar palabras negativas
            for keyword in keywords["negative"]:
                if keyword in text:
                    # Verificar contexto negativo
                    if f"no {keyword}" in text or f"sin {keyword}" in text:
                        score += 1
                    else:
                        score -= 1

            # Sólo añadir si hay cambio
            if score != 0:
                detected_attributes[attr] = score

        return detected_attributes

    def get_top_attributes(self, count=3):
        """Obtiene los atributos con mayor valor"""
        sorted_attrs = sorted(self.attributes.items(), key=lambda x: abs(x[1]), reverse=True)
        return [attr[0] for attr in sorted_attrs[:count]]

    def check_consequences(self):
        """Verifica si hay consecuencias basadas en atributos"""
        consequences = []

        for attr, value in self.attributes.items():
            if value >= 5:
                consequences.append(self._generate_positive_consequence(attr))
            elif value <= -5:
                consequences.append(self._generate_negative_consequence(attr))

        return "\n".join(consequences) if consequences else ""

    def _generate_positive_consequence(self, attribute):
        consequences = {
            "valentía": "Tu valentía ha llamado la atención de Dumbledore. Te ofrece unirse a la Orden del Fénix.",
            "astucia": "Tu astucia ha impresionado a algunos Slytherin. Te invitan a unirte a su círculo.",
            "inteligencia": "Tu inteligencia te ha ganado acceso a la Sección Prohibida de la biblioteca.",
            "lealtad": "Tu lealtad ha ganado el respeto de tus compañeros. Ahora eres el líder de tu casa.",
            "creatividad": "Tu creatividad ha impresionado al profesor Flitwick. Te ofrece clases avanzadas."
        }

        return consequences.get(attribute, f"Tu alto nivel de {attribute} ha abierto nuevas oportunidades.")

    def _generate_negative_consequence(self, attribute):
        consequences = {
            "valentía": "Tu falta de valentía ha hecho que algunos Gryffindors te eviten.",
            "astucia": "Tu falta de astucia ha hecho que algunos Slytherins se aprovechen de ti.",
            "inteligencia": "Tu bajo rendimiento académico preocupa a los profesores.",
            "lealtad": "Tu falta de lealtad ha hecho que tus amigos desconfíen de ti.",
            "creatividad": "Tu falta de creatividad limita tus hechizos. Necesitas más práctica."
        }

        return consequences.get(attribute, f"Tu bajo nivel de {attribute} ha creado algunos obstáculos.")