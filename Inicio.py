import streamlit as st
from utils.visuals import load_custom_css, card

# Configuración de la página
st.set_page_config(
    page_title="Proyecto Integrador - Analítica de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar Estilos Premium
load_custom_css()

# --- Hero Section Superior ---
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">🚀 Proyecto Integrador: Analítica de Datos</h1>
    <h3 style="color: #eef2f7;">Transformando Información en Decisiones Estratégicas</h3>
    <p style="opacity: 0.8; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
        Análisis avanzado de rendimiento competitivo en la <b>Overwatch League (OWL)</b> utilizando 
        técnicas modernas de Ciencia de Datos aplicadas a eSports.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 1. Introducción y Objetivos ---
col_intro, col_obj = st.columns([1, 1], gap="large")

with col_intro:
    st.header("📖 Introducción")
    st.write("""
    Este proyecto aplica técnicas de **Analítica de Datos** para desglosar el rendimiento competitivo en la **Overwatch League**.  
    A través de este tablero, exploramos métricas de eSports para identificar cómo los equipos profesionales gestionan sus recursos, tiempos de ejecución y estrategias por mapa nacional e internacional.
    """)
    st.info("💡 **Dato clave:** En la analítica de eSports, la precisión en los tiempos de ronda puede definir la victoria o derrota de una temporada completa.")

with col_obj:
    st.header("🎯 Objetivos")
    st.markdown("""
    *   **General:** Implementar un sistema de análisis exploratorio interactivo que identifique patrones de rendimiento y eficiencia en las estadísticas competitivas de la OWL.
    *   **Específicos:**
        *   Detectar anomalías y asegurar la calidad de datos.
        *   Analizar tendencias de mapas y "metajuego".
        *   Comparar métricas clave por equipo y jugador.
    """)

st.divider()

# --- 3. Equipo de Trabajo (Integrantes) ---
st.header("👥 Equipo de Desarrollo")

integrantes = [
    {"nombre": "Juan Pablo Blandon Barbosa", "rol": "Data Scientist", "emoji": "👨‍🔬"},
    {"nombre": "Juan Ricardo Oquendo Alzate", "rol": "Engineer", "emoji": "👨‍💻"},
    {"nombre": "Thomas Echeverry Rios", "rol": "Architect", "emoji": "📐"},
    {"nombre": "Santiago Velez Gutierrez", "rol": "Front-End", "emoji": "🎨"},
]

cols_team = st.columns(len(integrantes))

for i, persona in enumerate(integrantes):
    with cols_team[i]:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; border-bottom: 4px solid #0072ff; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{persona['emoji']}</div>
            <h4 style="margin: 5px 0;">{persona['nombre'].split(',')[0]}</h4>
            <p style="color: #666; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; margin: 0;">{persona['rol']}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# --- 4. Tecnologías ---
st.header("🛠 Ecosistema Tecnológico")

t1, t2, t3 = st.columns(3)

with t1:
    card("Python 🐍", "Lenguaje base para el procesamiento y lógica robusta del proyecto.", "🐍")

with t2:
    card("Pandas 🐼", "Librería líder para manipulación de DataFrames y limpieza masiva.", "🐼")

with t3:
    card("Streamlit 🔥", "Framework de vanguardia para desplegar dashboards interactivos velozmente.", "📊")

# --- Pie de página ---
st.sidebar.success("💡 Usa el menú lateral para navegar entre las secciones del proyecto.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Proyecto Integrador de Analítica")