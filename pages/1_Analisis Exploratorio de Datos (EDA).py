"""
1_Analisis Exploratorio de Datos (EDA).py
=========================================
Página 1 del proyecto multipágina: "Análisis Exploratorio de Datos"

Responsabilidades:
- Cargar dataset
- Mostrar estructura y contenido
- Estadísticas descriptivas
- Previsualización
"""

import sys
import os
import streamlit as st
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.data_loader import load_owl_data, get_dataset_info
from utils.preprocessing import rename_columns_for_display
from utils.visuals import load_custom_css, card

st.set_page_config(page_title="EDA - Exploración de Datos", layout="wide")

st.title("🔍 Análisis Exploratorio de Datos (EDA)")

st.markdown(
    """
    Esta página permite explorar la estructura del dataset antes de realizar cualquier análisis avanzado.
    Se centra en los jugadores/héroes y sus estadísticas.
    """
)

# ───────── CARGA DEL DATASET ─────────
df = load_owl_data()
if df is None:
    st.stop()

df = rename_columns_for_display(df)

# ───────── INFORMACIÓN GENERAL ─────────
st.header("ℹ️ Información del Dataset")
info = get_dataset_info(df)
st.write(f"**Filas:** {info['filas']}")
st.write(f"**Columnas:** {info['columnas']}")
st.write(f"**Columnas Numéricas:** {info['cols_numericas']}")
st.write(f"**Columnas Categóricas:** {info['cols_categoricas']}")
st.write(f"**Total Nulos:** {info['nulos_total']}")

# ───────── PREVISUALIZACIÓN ─────────
st.header("👀 Previsualización de Datos")
st.dataframe(df.head(10), use_container_width=True)

# ───────── ESTADÍSTICAS NUMÉRICAS ─────────
st.header("📊 Estadísticas Descriptivas (Numéricas)")
st.dataframe(df.describe(include="number").T, use_container_width=True)

# ───────── ESTADÍSTICAS CATEGÓRICAS ─────────
st.header("📊 Estadísticas Descriptivas (Categóricas)")
st.dataframe(df.describe(include="object").T, use_container_width=True)

# ───────── CARDINALIDAD Y NULOS ─────────
st.header("📌 Cardinalidad de Columnas Categóricas")
for col in info['cols_categoricas']:
    st.write(f"**{col}** → {df[col].nunique()} valores únicos")

st.header("⚠️ Nulos por Columna")
st.dataframe(df.isnull().sum(), use_container_width=True)