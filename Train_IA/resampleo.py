# resampleo.py

import pandas as pd

def resamplear_a_15min(df_limpio, config_entrenamiento):
    freq = config_entrenamiento["frecuencia_resampleo"]
    cols_media = [
        c for c in config_entrenamiento["columnas_agregacion_media"]
        if c in df_limpio.columns
    ]
    cols_max = [
        c for c in config_entrenamiento["columnas_agregacion_max"]
        if c in df_limpio.columns
    ]

    if not cols_media and not cols_max:
        raise ValueError(
            "Ninguna columna esperada en config_entrenamiento coincide "
            "con las columnas del DataFrame limpio. Revisa nombres."
        )

    partes = []
    if cols_media:
        partes.append(df_limpio[cols_media].resample(freq).mean())
    if cols_max:
        partes.append(df_limpio[cols_max].resample(freq).max())

    df_resampleado = pd.concat(partes, axis=1)

    orden_original = [c for c in df_limpio.columns if c in df_resampleado.columns]
    df_resampleado = df_resampleado[orden_original]

    return df_resampleado