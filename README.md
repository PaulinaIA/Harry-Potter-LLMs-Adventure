# 🧙‍♂️ Aventura en el Mundo de Harry Potter: Un Experimento de IA Narrativa

## [PROYECTO EN DESARROLLO]

Este repositorio contiene un prototipo de investigación en el campo de la IA narrativa y los sistemas conversacionales, usando el universo de Harry Potter como dominio temático. El proyecto explora la aplicación de modelos de lenguaje de gran escala (LLM) para la generación de narrativas interactivas y adaptativas, creando un marco de trabajo para estudiar la interacción humano-IA en contextos de narración.

## 🔬 Enfoque Experimental

Este trabajo se encuentra **en fase de desarrollo activo** y constituye una exploración de varios conceptos:

1. **Modelado contextual narrativo**: Análisis de cómo los LLM mantienen coherencia narrativa a lo largo de interacciones extendidas
2. **Construcción de personajes mediante prompting**: Métodos para mantener consistencia en las personalidades generadas por IA
3. **Extracción e interpretación de rasgos psicológicos**: Sistemas para inferir características de personalidad a partir de interacciones textuales
4. **Representación espacial y temporal en narrativas generadas**: Estructuras de datos para mantener coherencia en entornos ficticios
5. **Sistemas de memoria a largo plazo para agentes de IA**: Técnicas para almacenar y recuperar información contextual relevante

### Estado actual de la investigación

- ✅ Implementación del núcleo de IA conversacional
- ✅ Diseño del sistema de análisis de texto para extracción de atributos
- ✅ Prototipo de interfaz para interacción usuario-IA
- ✅ Sistemas básicos de gestión de estado del mundo
- 🔄 En desarrollo: Mejora de la coherencia narrativa a largo plazo
- 🔄 En desarrollo: Refinamiento del análisis semántico
- ⬜ Pendiente: Evaluación formal de la calidad narrativa
- ⬜ Pendiente: Estudios de usuario sobre inmersión e interactividad

## 📊 Fundamentos Técnicos

El experimento se basa en la hipótesis de que los modelos de lenguaje, con el contexto apropiado y sistemas de gestión de estado, pueden generar experiencias narrativas coherentes y personalizadas. El marco metodológico incluye:

### Arquitectura del Sistema

```
┌─────────────────────┐     ┌─────────────────────┐
│  Interfaz Usuario   │◄────┤ Procesador Prompts  │
└──────────┬──────────┘     └─────────┬───────────┘
           │                          │
           ▼                          ▼
┌─────────────────────┐     ┌─────────────────────┐
│    Modelo LLM       │◄────┤  Sistema Memoria    │
└──────────┬──────────┘     └─────────────────────┘
           │                          ▲
           ▼                          │
┌─────────────────────┐     ┌─────────────────────┐
│ Analizador Semántico│────►│ Gestor de Estado    │
└─────────────────────┘     └─────────────────────┘
```

### Componentes Principales de Investigación

1. **Sistema de Análisis Textual**
   - Análisis de patrones lingüísticos para identificar rasgos de personalidad
   - Extracción de decisiones narrativas relevantes
   - Implementado en `core/attributes.py`

2. **Memoria Contextual**
   - Representación vectorial de interacciones previas
   - Sistemas de priorización de información relevante
   - Implementado en `core/persistence.py`

3. **Gestión del Estado del Mundo**
   - Módulos para representar entornos narrativos coherentes
   - Sistemas para modelar causalidad y consecuencias
   - Implementados en diversos módulos bajo `core/`

4. **Prompt Engineering Avanzado**
   - Diseño de prompts para control narrativo
   - Técnicas de encuadre para mantener coherencia temática
   - Implementado en `app.py`

## 🛠️ Configuración del Entorno Experimental

### Requisitos

- Python 3.8+
- Acceso a modelos de lenguaje (local o API)
- Dependencias en `requirements.txt`

### Configuración del Modelo de Lenguaje

Este proyecto está diseñado para trabajar con diferentes arquitecturas de LLM:

#### Para experimentación local (recomendado):
```bash
# Instalación de Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo experimental
ollama pull llama3.2:1b

# Verificación
ollama run llama3.2:1b "Prueba de generación narrativa"
```

#### Para experimentación con modelos externos:
Configurar `config/settings.py` con los parámetros relevantes para el modelo a utilizar.

### Instalación del Entorno

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/harry-potter-adventure.git
cd harry-potter-adventure

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar experimento
python app.py
```

## 📓 Metodología Experimental

### Interacción con el Sistema

El usuario puede interactuar con el sistema a través de:

1. **Diálogo en lenguaje natural**
   - Permite la exploración libre de la narrativa
   - Facilita la recopilación de datos sobre patrones de interacción

2. **Comandos estructurados**
   - Prefijo `/` para acceder a funciones específicas
   - Permite mediciones controladas de comportamientos del sistema

### Variables de Observación

El sistema registra múltiples variables para análisis:

- Coherencia narrativa entre sesiones
- Consistencia de personajes generados
- Precisión en la extracción de atributos
- Adaptabilidad del sistema a diferentes estilos de juego
- Inmersión percibida por los usuarios

## 🔍 Estructura del Código Experimental

```
harry_potter_adventure_AI/
│
├── app.py                # Controlador principal del experimento
├── requirements.txt      # Dependencias
│
├── config/               # Parámetros experimentales
│   ├── hogwarts_theme.py # Configuración visual
│   └── settings.py       # Configuración del modelo LLM
│
├── core/                 # Módulos experimentales
│   ├── attributes.py     # Sistema de análisis semántico
│   ├── calendar.py       # Representación temporal
│   ├── characters.py     # Modelado de agentes narrativos
│   ├── events.py         # Generación de eventos narrativos
│   ├── locations.py      # Representación espacial
│   ├── persistence.py    # Sistema de memoria contextual
│   └── ...               # Otros módulos experimentales
│
└── ui/                   # Interfaz experimental
    └── interface.py      # Interfaz de observación
```

## 📈 Resultados Preliminares

Esta investigación se encuentra en su fase inicial y aún no hemos publicado resultados formales. Las observaciones preliminares sugieren:

- Los LLM pueden mantener coherencia narrativa con el apoyo de sistemas de memoria externa
- El análisis semántico permite extraer patrones de comportamiento del usuario
- La inmersión narrativa depende significativamente de la calidad del prompt inicial
- La consistencia del mundo generado requiere estructuras de datos específicas

## 🔮 Dirección Futura de la Investigación

Planeamos expandir este trabajo en varias direcciones:

- **Mejora de los sistemas de memoria contextual**: Implementación de sistemas de memoria a largo plazo más sofisticados
- **Evaluación formal**: Diseño de métricas para medir la calidad narrativa y la coherencia
- **Personalización adaptativa**: Desarrollo de sistemas que adapten la narrativa basándose en preferencias implícitas
- **Expansión del dominio narrativo**: Aplicación de la metodología a otros contextos narrativos
- **Estudio de interacción multimodal**: Incorporación de elementos visuales y auditivos

## 👥 Colaboración

Este es un proyecto de investigación abierto y acogemos colaboraciones, especialmente en las siguientes áreas:

- Mejora de los algoritmos de análisis semántico
- Optimización de prompts para mantener coherencia narrativa
- Diseño de experimentos para evaluar la calidad de la experiencia
- Expansión de los sistemas de representación del mundo

## 📄 Licencia

Este proyecto de investigación está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 📚 Referencias

[En desarrollo - Se añadirán referencias a trabajos relacionados en el campo de la IA narrativa, sistemas conversacionales y experiencias interactivas basadas en texto]

---

## 👩‍💻 Autora

**Paulina Peralta**

- GitHub: [PaulinaIA](https://github.com/PaulinaIA)
- Contacto: [pauliperalta97@gmail.com](mailto:pauliperalta97@gmail.com)

*Este trabajo representa un estudio en progreso sobre las capacidades de los modelos de lenguaje para la generación narrativa interactiva. Los resultados y observaciones son preliminares y sujetos a revisión.*
