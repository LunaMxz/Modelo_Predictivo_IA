"""
  Tipos inconsistentes (texto en campos numéricos)
  Fechas en formatos distintos
  Lecturas fuera de rango físico
  Códigos de error enmascarados (-999, 0 sospechoso)
  Picos de ruido imposibles (spikes)
  Registros duplicados
  Huecos temporales vía asfreq
  Nulos con relleno con promedio móvil centrado (lluvia: forward-fill aparte)
"""

import numpy as np
import pandas as pd


def normalizar_tipos_numericos(df, columnas):
    for col in columnas:
        if col not in df.columns:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[^\d\.,\-]", "", regex=True)  # quita °C, %, espacios, texto
                .str.replace(",", ".", regex=False)           # coma a . 
            )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def pipeline_limpieza_invernadero(df_crudo, config):
    df = df_crudo.copy()

    # Timestamp como índice datetime (acepta formatos mixtos: ISO, DD/MM/YYYY)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", dayfirst=True, errors="coerce")
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)  # asfreq y diff() requieren orden cronológico

    # Forzar tipos numéricos (por si el JSON trajo "24.1°C" o "60,5" como texto)
    df = normalizar_tipos_numericos(df, config["columnas_numericas"])

    # Eliminar registros duplicados de red
    df = df[~df.index.duplicated(keep="first")]

    # Reemplazar códigos de error de hardware por NaN
    df.replace(config["error_values"], np.nan, inplace=True)

    # Ceros sospechosos en columnas donde 0 real es casi imposible
    for col in config["columnas_cero"]:
        if col in df.columns:
            df.loc[df[col] == 0, col] = np.nan

    # Sincronizar el reloj (crea filas NaN en los huecos de red)
    df = df.asfreq(config["frecuencia_esperada"])

    # Filtrar valores fuera de rango físico
    for col, (minimo, maximo) in config["rangos_validos"].items():
        if col in df.columns:
            df.loc[~df[col].between(minimo, maximo), col] = np.nan

    # Filtrar picos (spike detection)
    for col, max_delta in config["max_delta_por_lectura"].items():
        if col in df.columns:
            df.loc[df[col].diff().abs() > max_delta, col] = np.nan

    # RELLENO INTELIGENTE: promedio móvil centrado, pero solo en huecos cuyo TAMAÑO TOTAL no exceda el límite.
    
    columnas_continuas = [c for c in config["rangos_validos"] if c != "lluvia_pct" and c in df.columns]
    promedio_movil = df[columnas_continuas].rolling(
        config["ventana_promedio_relleno"], center=True, min_periods=1
    ).mean()

    for col in columnas_continuas:
        es_nulo = df[col].isna()
        grupo_hueco = (es_nulo != es_nulo.shift()).cumsum()
        tamano_hueco = es_nulo.groupby(grupo_hueco).transform("sum")
        rellenable = es_nulo & (tamano_hueco <= config["limite_relleno"])
        df.loc[rellenable, col] = promedio_movil.loc[rellenable, col]

    # 7. Lluvia: nunca se promedia/interpola (es evento, no variable continua).
    #    Forward-fill corto; huecos largos quedan en NaN no "0%".
    if "lluvia_pct" in df.columns:
        df["lluvia_pct"] = df["lluvia_pct"].ffill(limit=config["limite_relleno_lluvia"])

    return df