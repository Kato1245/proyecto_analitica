import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Proyecto Integrador - Analítica de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo Personalizado (Opcional) ---
st.markdown("""
<style>
main {
    background-color: #f8f9fa;
}

.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- Título Principal ---
st.title("🚀 Proyecto Integrador: Analítica de Datos")
st.subheader("Transformando Información en Decisiones Estratégicas")

st.divider()

# --- 1. Introducción ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📖 Introducción")
    st.write("""
Este proyecto aplica técnicas de **Analítica de Datos** para desglosar el rendimiento competitivo en la **Overwatch League**.  
A través de este tablero, exploramos métricas de eSports para identificar cómo los equipos profesionales gestionan sus recursos, tiempos de ejecución y estrategias por mapa nacional e internacional.

Nuestro enfoque utiliza la **Exploración de Datos (EDA)** para transformar registros técnicos de partidas en conocimiento estratégico sobre el "metajuego" profesional.
""")

with col2:
    st.info("💡 **Dato:** En la analítica de eSports, la precisión en los tiempos de ronda puede definir la victoria o derrota de una temporada completa.")

# --- 2. Objetivos ---
st.header("🎯 Objetivos del Proyecto")

obj_gen, obj_esp = st.columns(2)

with obj_gen:
    st.subheader("Objetivo General")
    st.markdown("""
- Implementar un sistema de análisis exploratorio interactivo que identifique patrones de rendimiento y eficiencia en las estadísticas competitivas de la Overwatch League.
""")

with obj_esp:
    st.subheader("Objetivos Específicos")
    st.markdown("""
- Identificar anomalías en los registros técnicos de las partidas para asegurar la calidad de los datos de rendimiento.
- Analizar la frecuencia y éxito de los mapas competitivos para descifrar las tendencias de la liga.
- Utilizar estadísticas descriptivas para comparar métricas clave de jugadores y equipos.
- Evaluar la consistencia de los tiempos de ronda como indicador de equilibrio competitivo.
""")

st.divider()

# --- 3. Equipo de Trabajo ---
st.header("👥 Equipo de Trabajo (Integrantes)")

# Puedes ajustar los nombres aquí
integrantes = [
    {"nombre": "Juan Pablo Blandon Barbosa", "rol": "Analista de Datos", "emoji": "🧑‍💻"},
    {"nombre": "Juan Ricardo Oquendo Alzate", "rol": "Ingeniero de Datos", "emoji": "👨‍💻"},
    {"nombre": "Thomas Echeverry Rios", "rol": "Arquitecto de Soluciones", "emoji": "👨‍🔬"},
    {"nombre": "Santiago Velez Gutierrez", "rol": "Especialista en Front-End", "emoji": "👨‍🔬"},
]

cols = st.columns(len(integrantes))

for i, persona in enumerate(integrantes):
    with cols[i]:
        st.markdown(f"""
### {persona['emoji']} {persona['nombre']}
**Rol:** {persona['rol']}
""")

st.divider()

# --- 4. Tecnologías Utilizadas ---
st.header("🛠 Tecnologías")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("### 🐍 Python")
    st.write("Lenguaje base para el procesamiento y lógica del proyecto.")

with tech_col2:
    st.markdown("### 🐼 Pandas")
    st.write("Librería líder para manipulación y análisis de estructuras de datos.")

with tech_col3:
    st.markdown("### 📊 Streamlit")
    st.write("Framework para la creación de aplicaciones web interactivas de datos.")

# --- Pie de página ---
st.sidebar.success("💡 Usa el menú lateral para navegar entre las secciones del proyecto.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Proyecto Integrador de Analítica")