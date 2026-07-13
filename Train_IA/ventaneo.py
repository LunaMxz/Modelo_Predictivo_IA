# ventaneo.py

import numpy as np

def crear_ventanas(df_escalado, config_entrenamiento):
    lookback = config_entrenamiento["lookback_pasos"]
    horizon = config_entrenamiento["horizon_pasos"]
    targets = config_entrenamiento["targets"]

    columnas_features = (
        config_entrenamiento["columnas_agregacion_media"]
        + config_entrenamiento["columnas_agregacion_max"]
    )
    columnas_features = [c for c in columnas_features if c in df_escalado.columns]

    valores_x = df_escalado[columnas_features].values  # (n_filas, 4)
    valores_y = df_escalado[targets].values             # (n_filas, 3)

    n = len(df_escalado)
    n_muestras = n - lookback - horizon + 1
    if n_muestras <= 0:
        raise ValueError(
            f"Esta partición tiene {n} filas, insuficientes para "
            f"lookback={lookback} + horizon={horizon}. "
            f"Se necesitan al menos {lookback + horizon} filas."
        )

    # Ventanas de entrada: cada posición k=0..n_muestras-1 produce una
    # ventana con las filas [k, k+lookback)
    ventanas_x = np.lib.stride_tricks.sliding_window_view(
        valores_x, lookback, axis=0
    )  # shape: (n-lookback+1, features, lookback)
    ventanas_x = ventanas_x[:n_muestras].transpose(0, 2, 1).copy()
    # shape final: (n_muestras, lookback, n_features)

    # Ventanas de salida: para la muestra k, el target son las filas
    # [k+lookback, k+lookback+horizon) -- el futuro inmediato de esa ventana
    ventanas_y = np.lib.stride_tricks.sliding_window_view(
        valores_y, horizon, axis=0
    )  # shape: (n-horizon+1, n_targets, horizon)
    ventanas_y = ventanas_y[lookback:lookback + n_muestras].transpose(0, 2, 1).copy()
    # shape final: (n_muestras, horizon, n_targets)

    return ventanas_x, ventanas_y