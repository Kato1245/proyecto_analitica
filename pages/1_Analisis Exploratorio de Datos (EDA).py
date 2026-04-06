"""
1_Analisis Exploratorio de Datos (EDA).py
=========================================
Página 1 del proyecto multipágina: "Detective de Datos"
"""

import sys
import os
import streamlit as st
import pandas as pd

# ── Hack de importación para módulos utils ──────────────────────────────────
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.data_loader import load_owl_data, get_dataset_info
from utils.preprocessing import rename_columns_for_display
from utils.visuals import load_custom_css, card

# ── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis Exploratorio de Datos | OWL",
    page_icon="🔍",
    layout="wide",
)

# Cargar Estilos Premium
load_custom_css()

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
    st.warning("⚠️ **Nota:** En esta etapa, el reto es entender los datos solo con números y texto.")


# ── Carga de Datos ─────────────────────────────────────────────────────────
with st.status("📦 Cargando y procesando dataset de Overwatch League...", expanded=True) as status:
    df = load_owl_data()
    if df is not None:
        info = get_dataset_info(df)
        status.update(label="✅ Dataset cargado exitosamente.", state="complete", expanded=False)
    else:
        st.error("⚠️ No se pudo cargar el dataset. Verifica tu conexión o la instalación de kagglehub.")
        st.stop()

st.divider()

# ── STEP 1: Primer Impacto ─────────────────────────────────────────────────
st.header("📂 Step 1: Primer Impacto (Dataset Preview)")
st.markdown("Observa las **primeras 10 filas**. ¿Qué conceptos o palabras clave se repiten?")

# Contenedor con borde para el dataframe
with st.container():
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

c1, c2 = st.columns(2)

with c1:
    st.subheader("📏 Registro de Dimensiones")
    met1, met2 = st.columns(2)
    with met1:
        st.metric("Total de Filas", f"{info['filas']:,}")
    with met2:
        st.metric("Variables", info["columnas"])
    
    st.markdown("""
    <div style="background: #e1f5fe; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
        <b>💡 Tip:</b> Un volumen alto de filas indica que estamos ante un dataset 'macro' que cubre múltiples eventos.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.subheader("🔢 Tipos de Datos")
    dtypes_df = df.dtypes.rename("Tipo").to_frame()
    dtypes_df.index = [rename_columns_for_display(pd.DataFrame(columns=[col_name])).columns[0] for col_name in dtypes_df.index]
    st.dataframe(dtypes_df, use_container_width=True, height=250)

st.divider()

# ── STEP 3: Cardinalidad y Frecuencias ────────────────────────────────────
st.header("🃏 Step 3: Exploración de Categorías")

col_card, col_freq = st.columns([1, 1], gap="large")

with col_card:
    st.subheader("Valores Únicos")
    cat_cols = info["cols_categoricas"]
    if cat_cols:
        nunique_series = df[cat_cols].nunique().sort_values(ascending=False)
        nunique_df = nunique_series.reset_index()
        nunique_df.columns = ["Columna", "Uni"]
        nunique_df["Columna"] = nunique_df["Columna"].apply(lambda x: rename_columns_for_display(pd.DataFrame(columns=[x])).columns[0])
        st.dataframe(nunique_df, use_container_width=True)

with col_freq:
    st.subheader("Distribución de Valores")
    # Mapeo invertido para el selectbox
    display_cat_cols = [rename_columns_for_display(pd.DataFrame(columns=[c])).columns[0] for c in cat_cols] if cat_cols else []
    
    if display_cat_cols:
        selected_display_col = st.selectbox(
            "Selecciona columna:",
            options=display_cat_cols,
        )
        original_cat_col_selector = cat_cols[display_cat_cols.index(selected_display_col)]
        top_n = st.slider("Mostrar Top:", 5, 20, 10)
        vc = df[original_cat_col_selector].value_counts().head(top_n).reset_index()
        vc.columns = [selected_display_col, "Cantidad"]
        st.dataframe(vc, use_container_width=True)
    else:
        st.info("No hay columnas categóricas para mostrar.")

st.divider()

# ── STEP 4: Calidad ───────────────────────────────────────────────────────
st.header("❗ Step 4: Integridad de la Información")

missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({"Nulos": missing, "%": missing_pct})
missing_df = missing_df[missing_df["Nulos"] > 0].sort_values("Nulos", ascending=False)

if not missing_df.empty:
    st.warning(f"Se detectaron huecos de información en **{len(missing_df)} columnas**.")
    missing_df.index = [rename_columns_for_display(pd.DataFrame(columns=[c])).columns[0] for c in missing_df.index]
    st.dataframe(missing_df, use_container_width=True)
else:
    st.success("✅ Dataset íntegro: No se detectaron valores nulos.")

st.divider()

# ── STEP 5: Estadísticas ──────────────────────────────────────────────────
st.header("📊 Step 5: Análisis Descriptivo")

tab1, tab2 = st.tabs(["🔢 Numérico", "🏷️ Categórico"])

with tab1:
    st.dataframe(df.describe().round(2), use_container_width=True)

with tab2:
    cat_desc = df.describe(exclude=["number"])
    if not cat_desc.empty:
        st.dataframe(cat_desc, use_container_width=True)
    else:
        st.info("Resumen categórico no disponible.")

st.divider()

# ── Resumen ───────────────────────────────────────────────────────────────
st.header("🕵️ Informe del Detective")

res_col1, res_col2 = st.columns(2)

with res_col1:
    card("Calidad General", f"Se identificaron {info['nulos_total']:,} campos vacíos en total.", "🛡️")
with res_col2:
    ctx = ", ".join(info['cols_categoricas'][:3]) if info['cols_categoricas'] else "Desconocido"
    card("Contexto", f"Las variables sugeridas apuntan a un análisis de eSports profesional.", "🎮")