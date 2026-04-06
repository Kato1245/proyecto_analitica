"""
data_loader.py
==============
Módulo responsable de la carga del dataset desde Kaggle.
Utiliza @st.cache_data para evitar descargas redundantes entre páginas.
"""

import os
import streamlit as st
import pandas as pd
import kagglehub


@st.cache_data(show_spinner="📦 Descargando dataset de Overwatch League...")
def load_owl_data() -> pd.DataFrame | None:
    """
    Descarga y carga el dataset 'Overwatch League Stats Lab' desde Kaggle.

    - Busca automáticamente el CSV más relevante
    - Prioriza archivos de héroes o jugadores
    - Usa fallback inteligente si no encuentra
    """

    try:
        path = kagglehub.dataset_download("sherrytp/overwatch-league-stats-lab")
        csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]

        if not csv_files:
            st.error("❌ No se encontró ningún archivo CSV en el dataset descargado.")
            return None

        # 🔍 Mostrar todos los archivos encontrados
        st.write("📂 Archivos encontrados:", csv_files)

        csv_path = None

        # 🧠 PRIORIDAD 1: archivos de héroes o jugadores
        for file in csv_files:
            name = file.lower()
            if "hero" in name or "player" in name:
                csv_path = os.path.join(path, file)
                st.write("✅ Archivo seleccionado (héroes/jugadores):", file)
                break

        # 🟡 PRIORIDAD 2: archivo tipo phs (estadísticas de jugadores)
        if csv_path is None:
            for file in csv_files:
                name = file.lower()
                if "phs" in name:
                    csv_path = os.path.join(path, file)
                    st.write("⚠️ Archivo seleccionado (phs dataset):", file)
                    break

        # 🔴 PRIORIDAD 3: fallback a mapas o matches
        if csv_path is None:
            for file in csv_files:
                name = file.lower()
                if "match" in name or "map" in name:
                    csv_path = os.path.join(path, file)
                    st.write("⚠️ Archivo seleccionado (fallback match/map):", file)
                    break

        # 🔴 ÚLTIMO RECURSO
        if csv_path is None:
            csv_path = os.path.join(path, csv_files[0])
            st.write("⚠️ Archivo seleccionado (fallback general):", csv_files[0])

        # 📊 Cargar dataset
        df = pd.read_csv(csv_path, low_memory=False)

        # 🔍 Mostrar columnas para verificar contenido
        st.write("📊 Columnas del dataset:", df.columns.tolist())

        return df

    except Exception as e:
        st.error(f"❌ Error al cargar el dataset: {e}")
        return None


def get_dataset_info(df: pd.DataFrame) -> dict:
    """
    Genera un diccionario con información básica del dataset.
    """
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    return {
        "filas": df.shape[0],
        "columnas": df.shape[1],
        "cols_numericas": num_cols,
        "cols_categoricas": cat_cols,
        "nulos_total": df.isnull().sum().sum(),
    }