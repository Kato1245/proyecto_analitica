"""
2_Resultados (EDA).py
======================
Página 2 del proyecto multipágina: "Resultados del EDA"

Responsabilidades:
- Limpieza de datos
- Feature engineering
- Agrupaciones
- Visualización
"""

import sys
import os
import streamlit as st
import pandas as pd
import altair as alt

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.data_loader import load_owl_data
from utils.preprocessing import run_full_pipeline, rename_columns_for_display
from utils.analysis import (
    clasificar_estilo,
    meta_estilos,
    top_jugadores_por_categoria,
)
from utils.visuals import load_custom_css, card

st.set_page_config(page_title="Resultados del EDA", layout="wide")
st.title("📊 Resultados del EDA — Análisis Procesado")

st.markdown(
    """
    En esta página aplicamos el pipeline completo: 
    **limpieza → transformación → análisis → visualización interactiva.**
    """
)

# ───────── CARGA ─────────
df_raw = load_owl_data()
if df_raw is None:
    st.stop()

df_raw = rename_columns_for_display(df_raw)

# ───────── LIMPIEZA ─────────
df_clean, reporte = run_full_pipeline(df_raw)

# ───────── FEATURES ─────────
df_trabajo = df_clean.copy()

# ───────── ESTILO DE JUEGO ─────────
if "Estilo" not in df_trabajo.columns:
    df_trabajo["Estilo"] = df_trabajo["Nombre Estadística"].apply(clasificar_estilo)

# 🔹 Eliminar el rol Tanque completamente (según requerimiento previo)
df_trabajo = df_trabajo[df_trabajo["Estilo"] != "Tanque"].copy()

# ───────── BARRA LATERAL: FILTROS ─────────
with st.sidebar:
    st.header("🎯 Filtros de Análisis")
    if "Equipo" in df_trabajo.columns:
        equipos = sorted(df_trabajo["Equipo"].dropna().unique().tolist())
        equipo_sel = st.multiselect("Filtrar por Equipo:", equipos, default=equipos[:5])
        if equipo_sel:
            df_trabajo = df_trabajo[df_trabajo["Equipo"].isin(equipo_sel)]

    st.success(f"Analizando {len(df_trabajo):,} registros")

# ───────── META DEL JUEGO (ESTILO) ─────────
st.divider()
st.header("🎮 Meta del Juego (Distribución de Impacto)")

meta = meta_estilos(df_trabajo)
if meta is not None:
    col_meta_1, col_meta_2 = st.columns([1, 2])
    
    with col_meta_1:
        st.write("Impacto acumulado por cada estilo de juego detectado en las estadísticas:")
        st.dataframe(meta, use_container_width=True)
    
    with col_meta_2:
        # Gráfica de Donas con Altair
        donut = alt.Chart(meta).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Impacto Total", type="quantitative"),
            color=alt.Color(field="Estilo", type="nominal", scale=alt.Scale(scheme='category20b')),
            tooltip=["Estilo", "Impacto Total"]
        ).properties(title="Distribución de Impacto por Estilo")
        
        st.altair_chart(donut, use_container_width=True)
else:
    st.info("No se pudo generar el análisis de impacto. Revisa que el dataset tenga estadísticas de jugadores/héroes.")

# ───────── RANKING DE JUGADORES ─────────
st.divider()
st.header("🏆 Top Jugadores por Estilo")

# Columnas para mostrar
cols_muestra = ["Jugador", "Equipo", "Valor Estadística", "Nombre Estadística"]
roles = ["Daño", "Ofensivo", "Soporte"]

tabs = st.tabs([f"🎯 {r}" for r in roles])

for i, rol in enumerate(roles):
    with tabs[i]:
        df_rol = df_trabajo[df_trabajo["Estilo"] == rol].copy()
        
        if df_rol.empty:
            st.info(f"No hay datos para el rol {rol}.")
            continue
            
        # Top 10 jugadores general para este rol
        top_10 = df_rol.sort_values("Valor Estadística", ascending=False).head(10)
        
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.subheader(f"Top 10 en {rol}")
            st.dataframe(top_10[cols_muestra], use_container_width=True)
            
        with c2:
            # Gráfica de Barras Horizontal con Altair
            bar_chart = alt.Chart(top_10).mark_bar().encode(
                x=alt.X("Valor Estadística:Q", title="Valor de Estadística"),
                y=alt.Y("Jugador:N", sort="-x", title="Jugador"),
                color=alt.Color("Equipo:N", legend=None),
                tooltip=["Jugador", "Equipo", "Valor Estadística", "Nombre Estadística"]
            ).properties(height=300)
            
            st.altair_chart(bar_chart, use_container_width=True)

# ───────── COMPARATIVA DE EQUIPOS ─────────
st.divider()
st.header("📊 Comparativa de Rendimiento por Equipo")

if "Equipo" in df_trabajo.columns:
    st.write("Esta gráfica compara el rendimiento promedio que cada equipo tiene en los diferentes estilos de juego.")
    
    # Agrupamos por Equipo y Estilo para obtener el promedio
    df_equipo_impacto = df_trabajo.groupby(["Equipo", "Estilo"])["Valor Estadística"].mean().reset_index()
    
    # Gráfica de Barras Agrupadas con Altair
    grouped_bar = alt.Chart(df_equipo_impacto).mark_bar().encode(
        x=alt.X('Estilo:N', title=None),
        y=alt.Y('Valor Estadística:Q', title="Rendimiento Promedio"),
        color=alt.Color('Estilo:N', legend=alt.Legend(title="Estilo de Juego")),
        column=alt.Column('Equipo:N', title="Equipo", header=alt.Header(labelAngle=-45, labelFontSize=12)),
        tooltip=['Equipo', 'Estilo', 'Valor Estadística']
    ).properties(width=150, height=300)
    
    st.altair_chart(grouped_bar, use_container_width=False) # container_width=False for columns to work better
else:
    st.info("No hay datos de equipo suficientes para mostrar la comparativa.")
