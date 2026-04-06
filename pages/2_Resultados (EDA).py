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

st.set_page_config(page_title="Resultados del EDA", layout="wide")
st.title("📊 Resultados del EDA — Análisis Procesado")

st.markdown(
    """
    En esta página aplicamos el pipeline completo:
    limpieza → transformación → análisis → visualización.
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

# 🔹 Eliminar el rol Tanque completamente
df_trabajo = df_trabajo[df_trabajo["Estilo"] != "Tanque"].copy()

# ───────── META DEL JUEGO ─────────
st.divider()
st.header("🎮 Meta del Juego (Estilo de Juego)")

meta = meta_estilos(df_trabajo)
if meta is not None:
    st.dataframe(meta, use_container_width=True)
else:
    st.info("No se pudo generar el análisis de impacto. Revisa que el dataset tenga estadísticas de jugadores/héroes.")

# ───────── JUGADORES DESTACADOS POR ESTILO ─────────
st.divider()
st.header("🏆 Mejores Jugadores por Estilo y Equipo")

# ───────── TOP JUGADORES POR ROL ─────────
st.divider()
st.header("🏅 Mejores Jugadores por Rol y Equipo")

# Definimos los roles SIN tanque
roles = ["Daño", "Ofensivo", "Soporte"]

# Columnas que queremos mostrar para justificar por qué son los mejores
cols_muestra = ["Jugador", "Equipo", "Valor Estadística", "Nombre Estadística"]

for rol in roles:
    st.subheader(f"🎯 {rol}")
    
    # Filtramos por estilo
    df_rol = df_trabajo[df_trabajo["Estilo"] == rol].copy()
    
    if df_rol.empty:
        st.info(f"No hay datos para el rol {rol}.")
        continue
    
    # Seleccionamos el top jugador por equipo
    top_rol = (
        df_rol.loc[df_rol.groupby("Equipo")["Valor Estadística"].idxmax()]
        [cols_muestra]
        .sort_values("Equipo")
        .reset_index(drop=True)
    )
    
    st.dataframe(top_rol, use_container_width=True)