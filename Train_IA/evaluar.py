# evaluar.py
"""
Script de evaluacion FINAL -- no entrena nada, solo:
  1. Reconstruye la particion de test (necesita re-correr limpieza/
     resampleo/particion porque esos DataFrames nunca se guardaron en
     disco, a diferencia del modelo y el scaler que si se persistieron).
  2. Carga el modelo y el scaler YA ENTRENADOS desde artifacts/.
  3. Evalua en test y convierte metricas a unidades fisicas reales.
  4. Genera las alertas agronomicas para una muestra de ejemplo,
     usando la lluvia real (sin escalar) del final de su ventana de
     entrada.
"""

import sys
import os
import numpy as np
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
from evaluacion import evaluar_en_test
from motor_inferencia import generar_alertas


def main():
    # --- Reconstruir hasta la particion de test (sin volver a entrenar) ---
    print("Recargando y reprocesando datos hasta la particion de test...")
    df_crudo = cargar_desde_mysql()
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO)
    _, _, test = dividir_cronologico(df_15min, CONFIG_ENTRENAMIENTO)

    # --- Cargar el scaler YA AJUSTADO (no se vuelve a hacer fit) ---
    scaler = joblib.load("artifacts/scaler.pkl")
    test_esc = transformar_con_scaler_existente(test, scaler, CONFIG_ENTRENAMIENTO)

    # --- Ventanas escaladas (para el modelo) y crudas (para la lluvia real) ---
    X_test, y_test = crear_ventanas(test_esc, CONFIG_ENTRENAMIENTO)
    X_test_crudo, _ = crear_ventanas(test, CONFIG_ENTRENAMIENTO)  # sin escalar

    # --- Cargar el modelo YA ENTRENADO ---
    modelo = load_model("artifacts/modelo_gru.keras")

    # --- Evaluar en test + convertir a unidades fisicas reales ---
    predicciones_reales, y_test_reales = evaluar_en_test(
        modelo, X_test, y_test, scaler, CONFIG_ENTRENAMIENTO
    )

    # --- Generar alertas para la ULTIMA muestra de test (la mas reciente) ---
    columnas_orden = (
        CONFIG_ENTRENAMIENTO["columnas_agregacion_media"]
        + CONFIG_ENTRENAMIENTO["columnas_agregacion_max"]
    )
    idx_lluvia = columnas_orden.index("lluvia_pct")
    pasos_lluvia = CONFIG_ENTRENAMIENTO["pasos_lluvia_reciente"]

    i = -1  # ultima muestra disponible de test
    pred_temp = predicciones_reales[i, :, 0]
    pred_hum_ambiente = predicciones_reales[i, :, 1]
    pred_hum_suelo = predicciones_reales[i, :, 2]
    lluvia_reciente = X_test_crudo[i, -pasos_lluvia:, idx_lluvia]

    alertas = generar_alertas(
        pred_temp, pred_hum_ambiente, pred_hum_suelo,
        lluvia_reciente, CONFIG_ENTRENAMIENTO
    )

    print("\nAlertas para la ultima muestra de test:")
    print(alertas)

    return predicciones_reales, y_test_reales, alertas


if __name__ == "__main__":
    main()