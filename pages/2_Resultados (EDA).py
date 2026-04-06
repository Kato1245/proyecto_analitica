"""
2_Resultados (EDA).py
======================
Página 2 del proyecto multipágina: "Resultados del EDA"
"""

import sys
import os
import streamlit as st
import pandas as pd

# ── Importación local de módulos utils ─────────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.data_loader import load_owl_data
from utils.preprocessing import run_full_pipeline, rename_columns_for_display
from utils.analysis import (
    compute_round_metrics,
    groupby_map_type,
    groupby_map_name,
    groupby_team,
)
from utils.visuals import load_custom_css, card

# ── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Resultados del EDA | OWL",
    page_icon="📊",
    layout="wide",
)

# Cargar Estilos Premium
load_custom_css()

st.title("📊 Resultados del EDA — Análisis Procesado")
st.markdown(
    """
    En esta página aplicamos el **pipeline completo** de transformación:
    limpieza → feature engineering → agrupaciones → visualizaciones.
    """
)

# ── Carga de datos ─────────────────────────────────────────────────────────
df_raw = load_owl_data()

if df_raw is None:
    st.error("⚠️ Error crítico: No se pudo cargar el dataset.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1: Motor de Limpieza (Pipeline)
# ─────────────────────────────────────────────────────────────────────────────
st.header("🛠️ 1. Procesamiento de Datos")

with st.status("🚀 Ejecutando Pipeline de Limpieza...", expanded=True) as status:
    df_clean, reporte_limpieza = run_full_pipeline(df_raw)
    df_features = compute_round_metrics(df_clean)
    status.update(label="✅ Pipeline completado con éxito.", state="complete", expanded=False)

# Métricas visuales del proceso
cl1, cl2, cl3 = st.columns(3)
with cl1:
    st.metric("Filas Originales", f"{len(df_raw):,}")
with cl2:
    st.metric("Duplicados Removidos", reporte_limpieza["duplicados_eliminados"])
with cl3:
    st.metric("Nulos Corregidos", f"{reporte_limpieza['nulos_rellenados']:,}")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2: Panel de Filtros Interactivos
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")
    st.markdown("Ajusta los parámetros para el análisis dinámico.")
    
    df_trabajo = df_features.copy()

    # Filtro: Tipo de mapa
    if "map_type" in df_trabajo.columns:
        tipos = df_trabajo["map_type"].dropna().unique().tolist()
        tipos_sel = st.multiselect("Tipos de Mapa:", tipos, default=tipos)
        df_trabajo = df_trabajo[df_trabajo["map_type"].isin(tipos_sel)]

    # Filtro: Match ID (Slider)
    if "match_id" in df_trabajo.columns:
        id_min, id_max = int(df_trabajo["match_id"].min()), int(df_trabajo["match_id"].max())
        if id_min < id_max:
            range_sel = st.sidebar.slider("Match ID:", id_min, id_max, (id_min, id_max))
            df_trabajo = df_trabajo[df_trabajo["match_id"].between(range_sel[0], range_sel[1])]

    st.divider()
    st.info(f"📊 **{len(df_trabajo):,}** registros activos.")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3: Visualizaciones e Insights
# ─────────────────────────────────────────────────────────────────────────────
st.header("📈 2. Análisis e Insights Visuales")

tab_t, tab_m, tab_e = st.tabs(["🗺️ Tipo de Mapa", "📍 Top Mapas", "🛡️ Equipos"])

with tab_t:
    res_tipo = groupby_map_type(df_trabajo)
    if res_tipo is not None:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.dataframe(rename_columns_for_display(res_tipo), use_container_width=True)
        with c2:
            st.bar_chart(res_tipo["Total_Rondas"])
    else:
        st.info("Datos de tipo de mapa no disponibles.")

with tab_m:
    res_mapa = groupby_map_name(df_trabajo)
    if res_mapa is not None:
        st.markdown("### Frecuencia de Selección de Mapas")
        st.bar_chart(res_mapa["Total_Rondas"], color="#d4af37") # Color dorado OWL
        st.dataframe(rename_columns_for_display(res_mapa.T), use_container_width=True)

with tab_e:
    res_equipo = groupby_team(df_trabajo)
    if res_equipo is not None:
        st.markdown("### Top Equipos por Rondas Jugadas")
        st.dataframe(rename_columns_for_display(res_equipo), use_container_width=True)
        st.bar_chart(res_equipo["Total_Rondas"])

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4: Reporte Dinámico
# ─────────────────────────────────────────────────────────────────────────────
st.header("📝 3. Generador de Reporte Ejecutivo")

# Datos para el reporte
n_mapas = df_trabajo["map_name"].nunique() if "map_name" in df_trabajo.columns else 0
n_tot = len(df_trabajo)

reporte_txt = f"""# Reporte de Análisis OWL
**Volumen Procesado:** {n_tot:,} registros.
**Mapas Únicos:** {n_mapas}.

## Conclusión
El análisis muestra una alta consistencia en los datos tras el pipeline. 
Se recomienda profundizar en las estrategias de los equipos en mapas de tipo '{tipos_sel[0] if tipos_sel else 'N/A'}'.
"""

col_rep1, col_rep2 = st.columns([2, 1])

with col_rep1:
    st.markdown("""
    <div style="background: #f1f3f4; padding: 2rem; border-radius: 15px; border-left: 10px solid #0072ff;">
        <h3>Previsualización del Reporte</h3>
        <p>El reporte se genera basándose en los filtros actuales de la barra lateral.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.checkbox("Ver contenido del reporte"):
        st.markdown(reporte_txt)

with col_rep2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.download_button(
        "📥 Descargar Reporte (.md)",
        data=reporte_txt,
        file_name="reporte_owl_premium.md",
        use_container_width=True
    )
