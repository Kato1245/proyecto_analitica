import streamlit as st

# Configuración de la página
st.set_page_config(
   page_title="Plantilla de Resultados - Proyecto Analítica",
   page_icon="📝",
   layout="wide"
)

st.title("📝 Plantilla de Entrega: Resultados del EDA")
st.markdown("""
### Instrucciones
Utiliza esta página para documentar tus hallazgos. Completa cada sección basándote en lo que descubriste en la pestaña de *Análisis Exploratorio*.
Al finalizar, puedes previsualizar tu reporte consolidado.
""")

st.divider()

# --- Resultados del Análisis ---
with st.container():
   st.header("🔍 1. Identificación y Contexto")
   contexto = "El dataset 'Overwatch League Stats Lab' recopila información detallada sobre partidas competitivas de Overwatch a nivel profesional, incluyendo métricas de rendimiento de jugadores, tiempos de inicio de rondas y estadísticas por mapa. Su propósito es permitir el análisis profundo de la estrategia y evolución técnica de la liga profesional de eSports."
   st.info(contexto)

   st.header("❗ 2. Calidad de los Datos")
   calidad = "Se observa un dataset con un gran volumen de registros pero con desafíos en la serialización de tipos. Columnas como 'round_start_time' presentan tipos mixtos que requieren una limpieza previa (conversión a datetime y limpieza de strings) para su correcto procesamiento en herramientas de analítica moderna como PyArrow y Streamlit."
   st.warning(calidad)

   st.header("📈 3. Hallazgos Estadísticos Key")
   estadisticas = "Con miles de registros analizados, los hallazgos muestran una alta frecuencia de eventos en mapas específicos de Control y Escolta. La distribución de los tiempos de inicio de ronda sugiere una programación densa de partidas, con una variabilidad significativa que refleja el dinamismo de los encuentros competitivos."
   st.success(estadisticas)

   st.header("💡 4. Conclusión Final")
   conclusion = "El análisis revela que la analítica en eSports es una herramienta poderosa para entender el balance competitivo. Estos datos permiten identificar patrones ganadores y tendencias de juego que son fundamentales tanto para los equipos profesionales como para los desarrolladores en la toma de decisiones basada en evidencia."
   st.success(conclusion)

st.divider()

# --- Generación de Reporte ---
if st.button("🚀 Generar Previsualización del Reporte"):
   if contexto and calidad and estadisticas and conclusion:
       st.success("✅ Reporte Generado Exitosamente")
       
       reporte_md = f"""
       # Reporte de Análisis Exploratorio de Datos
       
       ## 1. Identificación y Contexto
       {contexto}
       
       ## 2. Calidad de los Datos
       {calidad}
       
       ## 3. Hallazgos Estadísticos Clave
       {estadisticas}
       
       ## 4. Conclusión Final
       {conclusion}
       
       ---
       Generado por el módulo de Reportes - Proyecto Integrador
        """
       
       st.markdown(reporte_md)
       st.download_button(
           label="📥 Descargar Reporte (.md)",
           data=reporte_md,
           file_name="reporte_eda_estudiante.md",
           mime="text/markdown"
       )
   else:
       st.warning("⚠️ Por favor, completa todas las secciones antes de generar el reporte.")

# --- Barra Lateral ---
st.sidebar.info("Esta es tu hoja de trabajo. Asegúrate de analizar bien los datos antes de escribir tus conclusiones.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Plantilla de Resultados")
