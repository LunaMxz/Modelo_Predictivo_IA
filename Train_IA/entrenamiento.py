# entrenamiento.py

import os
from tensorflow.keras.callbacks import EarlyStopping

def entrenar_modelo(modelo, X_train, y_train, X_val, y_val,
                     epochs_max=100, batch_size=32, patience=15,
                     ruta_guardado="artifacts/modelo_gru.keras"):

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=patience,
        restore_best_weights=True,
        verbose=1,
    )

    historia = modelo.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs_max,
        batch_size=batch_size,
        callbacks=[early_stopping],
        verbose=1,
    )

    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
    modelo.save(ruta_guardado)
    print(f"\nModelo guardado en: {ruta_guardado}")

    mejor_epoca = len(historia.history["loss"]) - patience
    print(f"Entrenamiento detenido en la época {len(historia.history['loss'])} "
          f"(mejor val_loss visto alrededor de la época {max(mejor_epoca, 1)})")

    return historia