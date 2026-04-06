"""
analysis.py
===========
Módulo de análisis y transformación del dataset Overwatch League.

Patrón adaptado de analisis-aroma-grano/app.py:
  - Ingreso_Bruto = precio * cantidad  →  compute_round_metrics() (métricas de rendimiento por ronda)
  - groupby('tipo').agg(...)           →  groupby_map_type(), groupby_map_name(), groupby_team()
"""

import pandas as pd


# ─── Feature Engineering ──────────────────────────────────────────────────────

def compute_round_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea métricas derivadas de rendimiento por ronda.

    Equivalente a 'Ingreso_Bruto = precio * cantidad' en app.py,
    pero adaptado al contexto de eSports OWL.

    Métricas creadas (si las columnas base existen):
      - 'Es_Overtime': bool → si la ronda llegó a tiempo extra
      - 'Mes': extraído de round_start_time (si está en datetime)

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame con nuevas columnas métricas.
    """
    df = df.copy()

    # Métrica: flag de overtime (si la columna 'attacker_payload_distance'
    # es mayor al percentil 90, se considera "extendida")
    if "attacker_payload_distance" in df.columns:
        p90 = df["attacker_payload_distance"].quantile(0.90)
        df["Ronda_Extendida"] = df["attacker_payload_distance"] >= p90

    # Métrica: mes de la partida para análisis temporal
    if "round_start_time" in df.columns:
        try:
            dt = pd.to_datetime(df["round_start_time"], errors="coerce", utc=True)
            df["Mes_Partida"] = dt.dt.strftime("%Y-%m")
        except Exception:
            pass

    return df


# ─── Agrupaciones (Equivalente a groupby en app.py) ───────────────────────────

def groupby_map_type(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    Agrupa por tipo de mapa y cuenta registros.
    Equivalente a: df.groupby('tipo')['Ingreso_Bruto'].agg([...])

    Returns
    -------
    pd.DataFrame | None
    """
    if "map_type" not in df.columns:
        return None

    resumen = (
        df.groupby("map_type")
        .agg(
            Total_Rondas=("map_type", "count"),
            Mapas_Únicos=("map_name", "nunique") if "map_name" in df.columns else ("map_type", "nunique"),
        )
        .sort_values("Total_Rondas", ascending=False)
        .round(2)
    )
    return resumen


def groupby_map_name(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    Agrupa por nombre de mapa. Top de mapas más jugados.

    Returns
    -------
    pd.DataFrame | None
    """
    if "map_name" not in df.columns:
        return None

    resumen = (
        df.groupby("map_name")
        .agg(Total_Rondas=("map_name", "count"))
        .sort_values("Total_Rondas", ascending=False)
        .head(15)
    )
    return resumen


def groupby_team(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    Agrupa por equipo atacante o local si la columna existe.

    Returns
    -------
    pd.DataFrame | None
    """
    team_col = None
    for candidate in ["attacker_name", "team_name", "attacker_team_name"]:
        if candidate in df.columns:
            team_col = candidate
            break

    if team_col is None:
        return None

    resumen = (
        df.groupby(team_col)
        .agg(Total_Rondas=(team_col, "count"))
        .sort_values("Total_Rondas", ascending=False)
        .head(15)
        .rename_axis("Equipo")
    )
    return resumen


def get_value_counts(df: pd.DataFrame, col: str, top_n: int = 15) -> pd.DataFrame:
    """
    Retorna el value_counts de una columna como DataFrame.
    Adaptado de: df['producto'].value_counts()

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        Nombre de la columna.
    top_n : int
        Cantidad máxima de valores a retornar.

    Returns
    -------
    pd.DataFrame
    """
    if col not in df.columns:
        return pd.DataFrame()

    result = (
        df[col]
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    result.columns = [col, "Frecuencia"]
    return result

#eso es todo