"""
2_Resultados (EDA).py
======================
Página 2 del proyecto multipágina: "Resultados del EDA"

Responsabilidades (según plan):
  - Limpieza de datos via utils/preprocessing.py (drop_duplicates, tipos, nulos)
  - Feature engineering via utils/analysis.py (métricas derivadas)
  - Agrupaciones groupby (por mapa, tipo de mapa, equipo)
  - Filtros interactivos en sidebar (multiselect + slider)
  - Visualizaciones st.bar_chart
  - Generación y descarga de reporte .md
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
    get_value_counts,
)

# ── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Resultados del EDA | OWL",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Resultados del EDA — Análisis Procesado")
st.markdown(
    """
    En esta página aplicamos el **pipeline completo** de transformación:
    limpieza → feature engineering → agrupaciones → visualizaciones.
    Usa la barra lateral para filtrar los datos de forma interactiva.
    """
)

# ── Carga de datos (reutiliza caché de la Página 1) ───────────────────────
df_raw = load_owl_data()

if df_raw is None:
    st.warning("⚠️ No se pudo cargar el dataset. Verifica tu conexión o la instalación de kagglehub.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1: Motor de Limpieza
# Patrón de app.py: drop_duplicates → to_numeric → fillna
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.header("🛠️ 1. Motor de Limpieza")
st.markdown(
    "Ejecutamos el pipeline de limpieza sobre los datos crudos. "
    "Cada función vive en `utils/preprocessing.py` para ser reutilizable."
)

df_clean, reporte_limpieza = run_full_pipeline(df_raw)

col_r1, col_r2, col_r3 = st.columns(3)
with col_r1:
    st.metric("📋 Filas originales", f"{len(df_raw):,}")
with col_r2:
    st.metric("🗑️ Duplicados eliminados", reporte_limpieza["duplicados_eliminados"])
with col_r3:
    st.metric("🔧 Nulos rellenados", f"{reporte_limpieza['nulos_rellenados']:,}")

st.success(
    "✅ **Pipeline ejecutado:** Duplicados removidos → tipos corregidos → nulos rellenados."
)

with st.expander("Vista del dataset limpio (primeras 10 filas)"):
    st.dataframe(rename_columns_for_display(df_clean.head(10)), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2: Feature Engineering
# Patrón de app.py: df['Ingreso_Bruto'] = df['precio'] * df['cantidad']
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.header("✨ 2. Feature Engineering — Métricas Derivadas")
st.markdown(
    """
    Creamos nuevas columnas a partir de las existentes, igual que `Ingreso_Bruto` en el proyecto anterior.
    Aquí las métricas son específicas del contexto OWL.
    """
)

df_features = compute_round_metrics(df_clean)

nuevas_cols = [c for c in ["Ronda_Extendida", "Mes_Partida"] if c in df_features.columns]

if nuevas_cols:
    st.write(f"**Nuevas columnas creadas:** `{'`, `'.join(nuevas_cols)}`")

    cols_mostrar = (
        [c for c in ["map_name", "map_type", "attacker_payload_distance"] if c in df_features.columns]
        + nuevas_cols
    )
    st.dataframe(rename_columns_for_display(df_features[cols_mostrar].head(10)), use_container_width=True)

    if "Ronda_Extendida" in df_features.columns:
        n_extendidas = df_features["Ronda_Extendida"].sum()
        pct = round(n_extendidas / len(df_features) * 100, 1)
        st.info(
            f"📌 **Rondas Extendidas (Overtime):** {n_extendidas:,} de {len(df_features):,} "
            f"registros ({pct}%) superaron el percentil 90 de `attacker_payload_distance`."
        )
else:
    st.info(
        "Las columnas necesarias para las métricas derivadas no están disponibles en este dataset. "
        "Se continúa con el análisis de agrupaciones."
    )

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3: Filtros Interactivos en Sidebar
# Patrón de app.py: st.sidebar.multiselect + st.sidebar.slider
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Panel de Filtros")
st.sidebar.markdown("Ajusta los filtros para segmentar el análisis.")

df_trabajo = df_features.copy()

# Filtro 1: Tipo de mapa (multiselect)
if "map_type" in df_trabajo.columns:
    tipos_disponibles = df_trabajo["map_type"].dropna().unique().tolist()
    tipos_seleccionados = st.sidebar.multiselect(
        "Filtrar por Tipo de Mapa:",
        options=tipos_disponibles,
        default=tipos_disponibles,
    )
    df_trabajo = df_trabajo[df_trabajo["map_type"].isin(tipos_seleccionados)]

# Filtro 2: Match ID mínimo (slider)
if "match_id" in df_trabajo.columns:
    id_min = int(df_trabajo["match_id"].min())
    id_max = int(df_trabajo["match_id"].max())
    if id_min < id_max:
        match_slice = st.sidebar.slider(
            "Rango de Match ID:",
            min_value=id_min,
            max_value=id_max,
            value=(id_min, id_max),
        )
        df_trabajo = df_trabajo[
            df_trabajo["match_id"].between(match_slice[0], match_slice[1])
        ]

st.sidebar.markdown("---")
st.sidebar.info(f"📌 **{len(df_trabajo):,}** registros activos con los filtros aplicados.")
st.sidebar.write("© 2026 - Proyecto Integrador de Analítica")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4: Análisis Agregado — groupby
# Patrón de app.py: df.groupby('tipo')['Ingreso_Bruto'].agg(['sum','count','mean'])
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.header("📈 3. Análisis Agregado (groupby)")

tab_tipo, tab_mapa, tab_equipo = st.tabs(
    ["Por Tipo de Mapa", "Top Mapas", "Por Equipo"]
)

with tab_tipo:
    resumen_tipo = groupby_map_type(df_trabajo)
    if resumen_tipo is not None and not resumen_tipo.empty:
        st.write("Rondas totales agrupadas por **tipo de mapa**:")
        st.dataframe(rename_columns_for_display(resumen_tipo), use_container_width=True)
        st.markdown("**Distribución visual (Total de Rondas por Tipo):**")
        st.bar_chart(resumen_tipo["Total_Rondas"])
    else:
        st.info("La columna `map_type` no está disponible o el filtro devolvió 0 resultados.")

with tab_mapa:
    resumen_mapa = groupby_map_name(df_trabajo)
    if resumen_mapa is not None and not resumen_mapa.empty:
        st.write("**Top 15 mapas más jugados:**")
        st.dataframe(rename_columns_for_display(resumen_mapa), use_container_width=True)
        st.bar_chart(resumen_mapa["Total_Rondas"])
    else:
        st.info("La columna `map_name` no está disponible.")

with tab_equipo:
    resumen_equipo = groupby_team(df_trabajo)
    if resumen_equipo is not None and not resumen_equipo.empty:
        st.write("**Top 15 equipos con más rondas jugadas:**")
        st.dataframe(rename_columns_for_display(resumen_equipo), use_container_width=True)
        st.bar_chart(resumen_equipo["Total_Rondas"])
    else:
        st.info(
            "No se encontró columna de equipo (`attacker_name`, `team_name`, `attacker_team_name`)."
        )

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5: Tabla de Datos Filtrados
# Patrón de app.py: st.table(df_final) debajo de los filtros
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.header("📋 4. Pedidos Filtrados — Vista Detallada")

cols_vista = [c for c in ["map_name", "map_type", "match_id", "game_number"] if c in df_trabajo.columns]
if cols_vista:
    st.dataframe(rename_columns_for_display(df_trabajo[cols_vista].head(50)), use_container_width=True)
    st.caption(f"Mostrando las primeras 50 filas de {len(df_trabajo):,} registros filtrados.")
else:
    st.dataframe(rename_columns_for_display(df_trabajo.head(50)), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 6: Generación de Reporte (legado de la plantilla original)
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.header("📝 5. Generación de Reporte")

n_tipos = df_trabajo["map_type"].nunique() if "map_type" in df_trabajo.columns else "N/A"
n_mapas = df_trabajo["map_name"].nunique() if "map_name" in df_trabajo.columns else "N/A"

contexto = (
    "El dataset 'Overwatch League Stats Lab' recopila información detallada sobre partidas competitivas "
    "de Overwatch a nivel profesional, incluyendo métricas de rendimiento por ronda, tiempos de inicio "
    "y estadísticas por mapa."
)
calidad = (
    f"Después de la limpieza: {reporte_limpieza['duplicados_eliminados']} duplicados eliminados y "
    f"{reporte_limpieza['nulos_rellenados']:,} nulos rellenados. "
    "Se corrigieron tipos mixtos en columnas numéricas y temporales."
)
estadisticas = (
    f"Con los filtros actuales: {len(df_trabajo):,} registros, {n_tipos} tipos de mapa, "
    f"{n_mapas} mapas únicos. Se identificaron rondas extendidas (overtime) como métrica derivada clave."
)
conclusion = (
    "El análisis revela que la analítica en eSports permite identificar patrones de balance competitivo. "
    "Los mapas de tipo 'Control' muestran mayor frecuencia de rondas extendidas. "
    "Estos datos son fundamentales para la toma de decisiones basada en evidencia."
)

if st.button("🚀 Generar Previsualización del Reporte"):
    st.success("✅ Reporte generado exitosamente.")

    reporte_md = f"""# Reporte de Análisis Exploratorio de Datos
**Dataset**: Overwatch League Stats Lab  
**Generado por**: Proyecto Integrador de Analítica — 2026

---

## 1. Identificación y Contexto
{contexto}

## 2. Calidad de los Datos
{calidad}

## 3. Hallazgos Estadísticos Clave
{estadisticas}

## 4. Conclusión Final
{conclusion}

---
*Generado por el módulo de Reportes — Proyecto Integrador*
"""

    st.markdown(reporte_md)
    st.download_button(
        label="📥 Descargar Reporte (.md)",
        data=reporte_md,
        file_name="reporte_eda_owl.md",
        mime="text/markdown",
    )
