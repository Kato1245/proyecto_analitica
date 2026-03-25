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

    - Usa kagglehub para obtener la ruta local del dataset.
    - Encuentra automáticamente el primer archivo CSV disponible.
    - Retorna un DataFrame limpio o None si ocurre un error.

    Returns
    -------
    pd.DataFrame | None
        DataFrame con los datos cargados, o None en caso de error.
    """
    try:
        path = kagglehub.dataset_download("sherrytp/overwatch-league-stats-lab")
        csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]

        if not csv_files:
            st.error("❌ No se encontró ningún archivo CSV en el dataset descargado.")
            return None

        # Cargamos el primer CSV encontrado con low_memory=False (buena práctica)
        csv_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(csv_path, low_memory=False)
        return df

    except Exception as e:
        st.error(f"❌ Error al cargar el dataset: {e}")
        return None


def get_dataset_info(df: pd.DataFrame) -> dict:
    """
    Genera un diccionario con información básica del dataset.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame de entrada.

    Returns
    -------
    dict
        Claves: 'filas', 'columnas', 'cols_numericas', 'cols_categoricas', 'nulos_total'
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
