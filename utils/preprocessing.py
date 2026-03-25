"""
preprocessing.py
================
Módulo de limpieza y preparación del dataset Overwatch League.

Patrón adaptado de analisis-aroma-grano/app.py:
  - drop_duplicates  →  remove_duplicates()
  - pd.to_numeric    →  fix_numeric_columns()
  - fillna           →  handle_nulls()
"""

import pandas as pd


# Columnas que deberían ser numéricas pero pueden venir como texto
NUMERIC_COLS = [
    "match_id",
    "game_number",
    "round_number",
]

# Columna de tiempo que a veces tiene tipos mixtos
DATETIME_COLS = ["round_start_time"]


def remove_duplicates(df: pd.DataFrame, subset: list | None = None) -> pd.DataFrame:
    """
    Elimina filas duplicadas del DataFrame.

    Si no se especifica subset, usa todas las columnas.
    Equivalente a df.drop_duplicates(subset=['id']) en app.py.

    Parameters
    ----------
    df : pd.DataFrame
    subset : list | None
        Columnas a considerar para detectar duplicados.

    Returns
    -------
    pd.DataFrame
        DataFrame sin duplicados.
    """
    filas_antes = len(df)
    df_clean = df.drop_duplicates(subset=subset)
    filas_despues = len(df_clean)
    filas_eliminadas = filas_antes - filas_despues
    return df_clean, filas_eliminadas


def fix_numeric_columns(df: pd.DataFrame, cols: list | None = None) -> pd.DataFrame:
    """
    Convierte columnas al tipo numérico usando errors='coerce'.
    Los valores no convertibles se transforman en NaN.

    Adaptado de: df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')

    Parameters
    ----------
    df : pd.DataFrame
    cols : list | None
        Columnas a convertir. Por defecto: NUMERIC_COLS del módulo.

    Returns
    -------
    pd.DataFrame
    """
    target_cols = cols if cols is not None else NUMERIC_COLS
    df = df.copy()

    for col in target_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def fix_datetime_columns(df: pd.DataFrame, cols: list | None = None) -> pd.DataFrame:
    """
    Convierte columnas de tiempo al tipo datetime con errors='coerce'.
    Necesario para el dataset OWL donde round_start_time tiene tipos mixtos.

    Parameters
    ----------
    df : pd.DataFrame
    cols : list | None
        Columnas a convertir. Por defecto: DATETIME_COLS del módulo.

    Returns
    -------
    pd.DataFrame
    """
    target_cols = cols if cols is not None else DATETIME_COLS
    df = df.copy()

    for col in target_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

    return df


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estrategia de manejo de nulos:
    - Columnas numéricas: rellena con la mediana de la columna.
    - Columnas categóricas: rellena con 'Desconocido'.

    Adaptado de: df['cantidad'] = df['cantidad'].fillna(1)

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    df = df.copy()

    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(exclude="number").columns:
        df[col] = df[col].fillna("Desconocido")

    return df


# ── Mapa de renombrado de columnas (inglés → español legible) ─────────────────
COLUMN_RENAME = {
    # ── Identificadores generales ──────────────────────────────────────────
    "match_id":                         "ID Partida",
    "esports_match_id":                 "ID eSports",
    "game_number":                      "N° Juego",
    "round_number":                     "N° Ronda",
    "round_start_time":                 "Inicio de Ronda",
    "game_version":                     "Versión del Juego",

    # ── Torneo / Etapa ─────────────────────────────────────────────────────
    "tournament_title":                 "Torneo",
    "stage":                            "Etapa",
    "season":                           "Temporada",
    "match_date":                       "Fecha de Partida",

    # ── Mapa ───────────────────────────────────────────────────────────────
    "map_name":                         "Mapa",
    "map_type":                         "Tipo de Mapa",
    "control_map_time":                 "Tiempo de Control en Mapa",
    "has_draw":                         "¿Hubo Empate?",

    # ── Equipos ────────────────────────────────────────────────────────────
    "team_name":                        "Equipo",
    "team_one_name":                    "Equipo Local",
    "team_two_name":                    "Equipo Visitante",
    "attacker_name":                    "Equipo Atacante",
    "attacker_team_name":               "Equipo Atacante",
    "defender_name":                    "Equipo Defensor",
    "defender_team_name":               "Equipo Defensor",
    "match_winner":                     "Ganador de Partida",
    "map_winner":                       "Ganador de Mapa",
    "map_loser":                        "Perdedor de Mapa",

    # ── Jugadores y Héroes ─────────────────────────────────────────────────
    "player_name":                      "Jugador",
    "player":                           "Jugador",
    "hero":                             "Héroe",
    "hero_name":                        "Héroe",
    "hero_time_played":                 "Tiempo Jugado (Héroe)",

    # ── Estadísticas de jugador ────────────────────────────────────────────
    "stat_name":                        "Nombre Estadística",
    "stat_amount":                      "Valor Estadística",
    "eliminations":                     "Eliminaciones",
    "final_blows":                      "Golpes Finales",
    "deaths":                           "Muertes",
    "all_damage_dealt":                 "Daño Total Infligido",
    "barrier_damage_dealt":             "Daño a Barreras",
    "hero_damage_dealt":                "Daño a Héroes",
    "healing_dealt":                    "Curación Realizada",
    "healing_received":                 "Curación Recibida",
    "self_healing":                     "Auto-Curación",
    "damage_taken":                     "Daño Recibido",
    "damage_blocked":                   "Daño Bloqueado",
    "defensive_assists":                "Asistencias Defensivas",
    "offensive_assists":                "Asistencias Ofensivas",
    "ultimates_earned":                 "Definitivas Acumuladas",
    "ultimates_used":                   "Definitivas Usadas",
    "time_building_ultimate":           "Tiempo Cargando Definitiva",
    "time_holding_ultimate":            "Tiempo con Definitiva Lista",
    "solo_kills":                       "Kills en Solitario",
    "objective_kills":                  "Kills en Objetivo",
    "objective_time":                   "Tiempo en Objetivo",
    "time_played":                      "Tiempo Jugado",
    "time_played_live":                 "Tiempo Jugado (En Vivo)",

    # ── Métricas de ronda ──────────────────────────────────────────────────
    "attacker_payload_distance":        "Distancia Payload (Atacante)",
    "attacker_time_banked":             "Tiempo Guardado (Atacante)",
    "defender_time_banked":             "Tiempo Guardado (Defensor)",
    "attacker_round_end_score":         "Puntaje Final (Atacante)",
    "defender_round_end_score":         "Puntaje Final (Defensor)",
    "round_end_reason":                 "Motivo Fin de Ronda",

    # ── Columnas derivadas (creadas en analysis.py) ────────────────────────
    "Ronda_Extendida":                  "¿Ronda Extendida?",
    "Mes_Partida":                      "Mes de Partida",

    # ── Columnas de agrupación generadas ──────────────────────────────────
    "Total_Rondas":                     "Total de Rondas",
    "Mapas_Únicos":                     "Mapas Únicos",
    "Total_Rondas":                     "Total de Rondas",
}


def rename_columns_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renombra las columnas del DataFrame a nombres en español más legibles.

    Solo renombra las columnas que existen en el DataFrame;
    las que no están en el mapa se conservan tal cual.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Copia del DataFrame con columnas renombradas.
    """
    cols_a_renombrar = {k: v for k, v in COLUMN_RENAME.items() if k in df.columns}
    return df.rename(columns=cols_a_renombrar)


def run_full_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Ejecuta el pipeline completo de limpieza en orden:
      1. Eliminar duplicados
      2. Corregir columnas numéricas
      3. Corregir columnas datetime
      4. Manejar nulos

    Returns
    -------
    tuple[pd.DataFrame, dict]
        (DataFrame limpio, reporte de cambios con estadísticas)
    """
    reporte = {}

    df_clean, filas_dup = remove_duplicates(df)
    reporte["duplicados_eliminados"] = filas_dup

    df_clean = fix_numeric_columns(df_clean)
    df_clean = fix_datetime_columns(df_clean)

    nulos_antes = df_clean.isnull().sum().sum()
    df_clean = handle_nulls(df_clean)
    reporte["nulos_rellenados"] = nulos_antes

    return df_clean, reporte
