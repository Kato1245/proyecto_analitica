"""
analysis.py
============
Funciones de análisis para el proyecto Overwatch League.
Incluye métricas de rondas, agrupaciones por mapas y equipos,
así como análisis de meta y ranking de jugadores.
"""

import pandas as pd

# ── Clasificación de estilo de juego ──────────────────────────────
def clasificar_estilo(stat_name: str) -> str:
    stat_name = stat_name.lower()
    if "elimination" in stat_name or "final_blow" in stat_name:
        return "Ofensivo"
    elif "damage" in stat_name:
        return "Daño"
    elif "healing" in stat_name:
        return "Soporte"
    elif "block" in stat_name:
        return "Tanque"
    else:
        return "General"

# ── Agrupaciones y métricas ─────────────────────────────────────
def compute_round_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera métricas adicionales por ronda si se necesitan.
    """
    df = df.copy()
    # Puedes crear métricas derivadas aquí si quieres
    return df

def groupby_map_type(df: pd.DataFrame) -> pd.DataFrame | None:
    if "Tipo de Mapa" in df.columns:
        return df.groupby("Tipo de Mapa").size().reset_index(name="Total_Rondas")
    return None

def groupby_map_name(df: pd.DataFrame) -> pd.DataFrame | None:
    if "Mapa" in df.columns:
        return df.groupby("Mapa").size().reset_index(name="Total_Rondas")
    return None

def groupby_team(df: pd.DataFrame) -> pd.DataFrame | None:
    if "Equipo" in df.columns:
        return df.groupby("Equipo").size().reset_index(name="Total_Rondas")
    return None

# ── Meta del juego por estilo ────────────────────────────────────
def meta_estilos(df: pd.DataFrame) -> pd.DataFrame | None:
    if "Nombre Estadística" not in df.columns:
        return None
    df = df.copy()
    
    # Generar columna Estilo si no existe
    if "Estilo" not in df.columns:
        df["Estilo"] = df["Nombre Estadística"].apply(clasificar_estilo)
    
    # 🔹 Eliminar Tanque de meta
    df = df[df["Estilo"] != "Tanque"]
    
    return df.groupby("Estilo")["Valor Estadística"].sum().reset_index(name="Impacto Total")

# ── Top jugadores por categoría ─────────────────────────────────
def top_jugadores_por_categoria(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    Retorna el jugador con mayor estadística en cada Estilo.
    """
    if not {"Jugador", "Estilo", "Valor Estadística", "Equipo"}.issubset(df.columns):
        return None

    df = df.copy()
    top_players = (
        df.loc[df.groupby(["Equipo", "Estilo"])["Valor Estadística"].idxmax()]
        [["Equipo", "Jugador", "Estilo", "Valor Estadística"]]
        .reset_index(drop=True)
    )
    return top_players