"""
1_Analisis Exploratorio de Datos (EDA).py
=========================================
Página 1 del proyecto multipágina: "Detective de Datos"

Responsabilidades (según plan):
  - Carga de datos via utils/data_loader.py
  - Vista inicial del dataset (head, shape, dtypes)
  - Métricas de cardinalidad (nunique)
  - value_counts interactivo por columna seleccionada
  - Identificación y visualización de nulos
  - Estadísticas descriptivas (numéricas y categóricas)
"""

import sys
import os

import streamlit as st
import pandas as pd

# ── Hack de importación para módulos utils en Streamlit multipage ──────────
# Streamlit ejecuta las páginas con el CWD del runner, no del archivo .py.
# Añadir el directorio raíz del proyecto al path garantiza que 'utils' se encuentre.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.data_loader import load_owl_data, get_dataset_info
from utils.preprocessing import rename_columns_for_display

# ── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis Exploratorio de Datos | OWL",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Actividad: ¿De qué se tratan estos datos?")
st.markdown(
    """
    ### Objetivo de la Actividad
    Actúa como un **detective de datos**. A partir de las tablas y estadísticas de abajo,
    deduce el contexto, el origen y el propósito del dataset de la **Overwatch League**.
    """
)

# ── Barra Lateral: Guía del Estudiante ────────────────────────────────────
with st.sidebar:
    st.header("🧭 Guía para el Estudiante")
    st.info(
        """
        1. **Previsualiza**: ¿Hay nombres de equipos, mapas o fechas?
        2. **Inspecciona**: ¿Es un dataset pequeño o masivo?
        3. **Analiza Limpieza**: ¿Faltan muchos datos? ¿En qué columnas?
        4. **Deduce**: Usa las estadísticas para entender el "comportamiento" de los datos.
        """
    )
    st.warning("⚠️ En esta etapa, **no usamos gráficos**. El reto es entender solo con números y texto.")

# ── Carga de Datos ─────────────────────────────────────────────────────────
df = load_owl_data()

if df is None:
    st.warning("⚠️ No se pudo cargar el dataset. Verifica tu conexión o la instalación de kagglehub.")
    st.stop()

st.success("📂 Dataset cargado exitosamente.")
info = get_dataset_info(df)

st.divider()

# ── STEP 1: Primer Impacto ─────────────────────────────────────────────────
st.header("📂 Step 1: Primer Impacto (Dataset Preview)")
st.markdown("Observa las **primeras 10 filas**. ¿Qué conceptos o palabras clave se repiten?")
st.dataframe(rename_columns_for_display(df.head(10)), use_container_width=True)

with st.expander("🧠 ¿Cómo interpreto este paso?"):
    st.write(
        """
        - **Nombres de columnas**: Son las 'etiquetas' de la información.
          `map_name` → hay mapas. `match_id` → hay partidas identificables.
        - **Valores iniciales**: ¿Son números, fechas o texto libre?
        - **Identificadores**: Columnas como `match_id` o `game_number` son llaves únicas.
        """
    )

st.divider()

# ── STEP 2: Estructura ─────────────────────────────────────────────────────
st.header("🏁 Step 2: La Estructura del Dataset")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📏 Dimensiones")
    st.metric("Total de Filas (registros)", f"{info['filas']:,}")
    st.metric("Total de Columnas (variables)", info["columnas"])
with col2:
    st.subheader("🔢 Tipos de Datos")
    dtypes_df = df.dtypes.rename("Tipo").to_frame()
    dtypes_df.index = [rename_columns_for_display(pd.DataFrame(columns=[col_name])).columns[0] for col_name in dtypes_df.index]
    st.dataframe(dtypes_df, use_container_width=True)

with st.expander("🧠 ¿Cómo interpreto la estructura?"):
    st.write(
        """
        - **Filas**: Cada fila = un evento de ronda en una partida profesional de OWL.
        - **`int64` / `float64`**: Columnas numéricas → permiten sumas, promedios.
        - **`object`**: Texto o categorías → equipos, mapas, tipos de mapa.
        - **`datetime64`**: Fechas → permiten análisis temporal por temporadas.
        """
    )

st.divider()

# ── STEP 3: Cardinalidad y Frecuencias ────────────────────────────────────
st.header("🃏 Step 3: Cardinalidad — ¿Cuántos valores únicos hay?")
st.markdown(
    "Equivalente a `df['col'].nunique()`. "
    "Muestra cuántos valores distintos existe en cada columna categórica."
)

cat_cols = info["cols_categoricas"]
if cat_cols:
    nunique_series = df[cat_cols].nunique().sort_values(ascending=False)
    nunique_df = nunique_series.reset_index()
    nunique_df.columns = ["Columna", "Valores Únicos"]
    nunique_df["Columna"] = nunique_df["Columna"].apply(lambda x: rename_columns_for_display(pd.DataFrame(columns=[x])).columns[0])
    st.dataframe(nunique_df, use_container_width=True)
else:
    st.info("No se encontraron columnas categóricas.")

st.markdown("---")
st.subheader("🔁 Frecuencias — value_counts interactivo")
st.markdown("Selecciona una columna para ver cuántas veces aparece cada valor.")

# Renombrar las opciones del selectbox para la visualización
display_cat_cols = [rename_columns_for_display(pd.DataFrame(columns=[c])).columns[0] for c in cat_cols] if cat_cols else []
selected_display_col = st.selectbox(
    "Columna para explorar frecuencias:",
    options=display_cat_cols if display_cat_cols else [rename_columns_for_display(pd.DataFrame(columns=[c])).columns[0] for c in df.columns.tolist()],
    index=0,
)
# Mapear de vuelta al nombre original de la columna para el dataframe
original_cat_col_selector = cat_cols[display_cat_cols.index(selected_display_col)] if cat_cols else df.columns.tolist()[display_cat_cols.index(selected_display_col)]


top_n = st.slider("Top N valores a mostrar:", min_value=5, max_value=30, value=15)

vc = df[original_cat_col_selector].value_counts().head(top_n).reset_index()
vc.columns = [selected_display_col, "Frecuencia"] # Use the display name for the column
st.dataframe(vc, use_container_width=True)

with st.expander("🧠 ¿Qué nos dice el value_counts?"):
    st.write(
        """
        - **Valor más frecuente (Moda)**: El registro más común. En OWL, probablemente sea el mapa o equipo más jugado.
        - **Valores raros** (frecuencia ≤ 5): Pueden indicar errores de captura o datos atípicos.
        - **Distribución uniforme** (todos con frecuencia similar): Sugiere un torneo bien balanceado.
        """
    )

st.divider()

# ── STEP 4: Calidad — Valores Nulos ───────────────────────────────────────
st.header("❗ Step 4: Calidad de Datos — Valores Nulos")

missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({"Nulos": missing, "% del Total": missing_pct})
missing_df = missing_df[missing_df["Nulos"] > 0].sort_values("Nulos", ascending=False)

if not missing_df.empty:
    st.warning(f"⚠️ Se encontraron **{len(missing_df)} columnas** con datos faltantes.")
    # Renombrar índice para mostrar nombres en español
    missing_df.index = [
        rename_columns_for_display(pd.DataFrame(columns=[c])).columns[0]
        for c in missing_df.index
    ]
    st.dataframe(missing_df, use_container_width=True)
else:
    st.success("✅ ¡Increíble! Este dataset está completo. No hay valores nulos.")

with st.expander("🧠 ¿Qué significan los nulos?"):
    st.write(
        """
        - **NaN**: Información no recolectada o que no aplica en ese evento.
        - **Impacto**: Si `map_name` tiene muchos nulos, el análisis por mapa sería poco confiable.
        - **Estrategia**: En la siguiente página veremos cómo limpiar estos registros.
        """
    )

st.divider()

# ── STEP 5: Estadísticas Descriptivas ────────────────────────────────────
st.header("📊 Step 5: El Corazón de los Datos (Estadísticas)")

tab_num, tab_cat = st.tabs(["🔢 Columnas Numéricas", "🏷️ Columnas Categóricas"])

with tab_num:
    st.write("Resumen estadístico de las variables cuantitativas:")
    st.dataframe(df.describe().round(2), use_container_width=True)

    with st.expander("Guía de Estadísticas Numéricas"):
        st.write(
            """
            - **mean (Promedio)**: Valor central. ¿Es razonable para el contexto del juego?
            - **min / max**: Detecta outliers o errores de captura.
            - **std (Desviación estándar)**: Alta variabilidad = muchos tipos de ronda diferentes.
            - **50% (Mediana)**: Si difiere mucho del promedio, los datos están sesgados.
            """
        )

with tab_cat:
    cat_desc = df.describe(exclude=["number"])
    if not cat_desc.empty:
        st.write("Resumen de columnas de texto / categorías:")
        st.dataframe(cat_desc, use_container_width=True)

        with st.expander("Guía de Estadísticas Categóricas"):
            st.write(
                """
                - **unique**: Cuántas opciones distintas existen (ej: 20 equipos en OWL).
                - **top (Moda)**: El valor que más se repite. ¡Suele ser la clave del dataset!
                - **freq**: Cuántas veces aparece el valor `top`.
                """
            )
    else:
        st.info("No se detectaron columnas categóricas en el resumen.")

st.divider()

# ── Resumen del Detective ─────────────────────────────────────────────────
st.header("🕵️ Informe del Detective — Resumen de Hallazgos")

st.markdown(
    f"""
    Basado en tu investigación, aquí hay una validación de lo que descubriste:

    | Aspecto | Hallazgo |
    |---|---|
    | 📏 **Volumen** | **{info['filas']:,} registros** — visión {'global (macrodataset)' if info['filas'] > 10_000 else 'específica'} del fenómeno |
    | 🏷️ **Variables texto** | **{len(info['cols_categoricas'])} columnas** → definen el *qué* y el *dónde* |
    | 🔢 **Variables numéricas** | **{len(info['cols_numericas'])} columnas** → cuantifican el *cuánto* |
    | 🚨 **Calidad** | **{info['nulos_total']:,} nulos totales** en el dataset |
    | 🗺️ **Contexto sugerido** | Columnas como `{'`, `'.join(info['cols_categoricas'][:3])}` sugieren análisis de eventos competitivos por mapa y equipo |
    """
)