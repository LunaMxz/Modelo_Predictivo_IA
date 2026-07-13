# escalador.py

import os
import joblib
from sklearn.preprocessing import MinMaxScaler

def ajustar_y_transformar(train, val, test, config_entrenamiento,
                           ruta_guardado="artifacts/scaler.pkl"):
    columnas_esperadas = (
        config_entrenamiento["columnas_agregacion_media"]
        + config_entrenamiento["columnas_agregacion_max"]
    )
    columnas = [c for c in train.columns if c in columnas_esperadas]

    scaler = MinMaxScaler()
    scaler.fit(train[columnas])  # SOLO train, nunca val ni test

    train_esc = train.copy()
    val_esc = val.copy()
    test_esc = test.copy()

    train_esc[columnas] = scaler.transform(train[columnas])
    val_esc[columnas] = scaler.transform(val[columnas])
    test_esc[columnas] = scaler.transform(test[columnas])

    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
    joblib.dump(scaler, ruta_guardado)
    print(f"Escalador guardado en: {ruta_guardado} (necesario para "
          f"inverse_transform de las predicciones en producción)")

    return train_esc, val_esc, test_esc, scaler