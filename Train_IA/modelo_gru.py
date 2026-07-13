# modelo_gru.py

from tensorflow.keras import layers, models, optimizers

def construir_modelo_gru(config_entrenamiento):
    lookback = config_entrenamiento["lookback_pasos"]
    horizon = config_entrenamiento["horizon_pasos"]
    n_features = len(
        config_entrenamiento["columnas_agregacion_media"]
        + config_entrenamiento["columnas_agregacion_max"]
    )
    n_targets = len(config_entrenamiento["targets"])

    modelo = models.Sequential([
        layers.Input(shape=(lookback, n_features)),

        layers.GRU(32, return_sequences=True, recurrent_dropout=0.2),
        layers.GRU(16, return_sequences=False, recurrent_dropout=0.2),

        layers.Dense(horizon * n_targets),
        layers.Reshape((horizon, n_targets)),
    ])

    modelo.compile(
        optimizer=optimizers.Adam(),
        loss="mse",
        metrics=["mae"],
    )

    return modelo

if __name__ == "__main__":
    from config_entrenamiento import CONFIG_ENTRENAMIENTO
    modelo = construir_modelo_gru(CONFIG_ENTRENAMIENTO)
    modelo.summary()