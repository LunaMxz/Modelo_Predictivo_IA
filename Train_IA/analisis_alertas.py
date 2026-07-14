# analisis_alertas.py

import sys
import os
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(RAIZ_PROYECTO)

from config import CONFIG
from limpieza import pipeline_limpieza_invernadero
from conexionDB.carga_mysql import cargar_desde_mysql

from config_entrenamiento import CONFIG_ENTRENAMIENTO
from resampleo import resamplear_a_15min
from particion import dividir_cronologico
from escalador import transformar_con_scaler_existente
from ventaneo import crear_ventanas
from evaluacion import revertir_escala_targets
from motor_inferencia import generar_alertas


def main():
    print("Reconstruyendo datos hasta la particion de test...")
    df_crudo = cargar_desde_mysql()
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO)
    _, _, test = dividir_cronologico(df_15min, CONFIG_ENTRENAMIENTO)

    scaler = joblib.load("artifacts/scaler.pkl")
    test_esc = transformar_con_scaler_existente(test, scaler, CONFIG_ENTRENAMIENTO)

    X_test, y_test = crear_ventanas(test_esc, CONFIG_ENTRENAMIENTO)
    X_test_crudo, _ = crear_ventanas(test, CONFIG_ENTRENAMIENTO)

    modelo = load_model("artifacts/modelo_gru.keras")

    print(f"Generando predicciones para las {len(X_test)} muestras de test...")
    predicciones_escaladas = modelo.predict(X_test, verbose=0)
    predicciones_reales = revertir_escala_targets(
        predicciones_escaladas, scaler, CONFIG_ENTRENAMIENTO
    )

    columnas_orden = (
        CONFIG_ENTRENAMIENTO["columnas_agregacion_media"]
        + CONFIG_ENTRENAMIENTO["columnas_agregacion_max"]
    )
    idx_lluvia = columnas_orden.index("lluvia_pct")
    pasos_lluvia = CONFIG_ENTRENAMIENTO["pasos_lluvia_reciente"]
    lookback = CONFIG_ENTRENAMIENTO["lookback_pasos"]

    registros = []
    for i in range(len(X_test)):
        pred_temp = predicciones_reales[i, :, 0]
        pred_hum_ambiente = predicciones_reales[i, :, 1]
        pred_hum_suelo = predicciones_reales[i, :, 2]
        lluvia_reciente = X_test_crudo[i, -pasos_lluvia:, idx_lluvia]

        alertas = generar_alertas(
            pred_temp, pred_hum_ambiente, pred_hum_suelo,
            lluvia_reciente, CONFIG_ENTRENAMIENTO
        )
        # Timestamp del inicio del horizonte predicho para esta muestra
        timestamp_inicio_horizonte = test.index[lookback + i]
        registros.append({"timestamp": timestamp_inicio_horizonte, **alertas})

    df_alertas = pd.DataFrame(registros).set_index("timestamp")

    print("\n" + "=" * 50)
    print("RESUMEN -- frecuencia de cada alerta sobre TODO test")
    print("=" * 50)
    total = len(df_alertas)
    for columna in ["crecimiento_optimo", "estres_hidrico", "escudo_fungico"]:
        activaciones = df_alertas[columna].sum()
        porcentaje = 100 * activaciones / total
        print(f"{columna}: {activaciones}/{total} muestras ({porcentaje:.1f}%)")

    df_alertas.to_csv("artifacts/alertas_test.csv")
    print("\nDetalle completo guardado en: artifacts/alertas_test.csv")

    return df_alertas


if __name__ == "__main__":
    main()