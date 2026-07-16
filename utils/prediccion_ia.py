# utils/prediccion_ia.py


import numpy as np
import joblib
import streamlit as st

from config import CONFIG
from limpieza import pipeline_limpieza_invernadero

from Train_IA.config_entrenamiento import CONFIG_ENTRENAMIENTO
from Train_IA.resampleo import resamplear_a_15min
from Train_IA.escalador import transformar_con_scaler_existente
from Train_IA.evaluacion import revertir_escala_targets
from Train_IA.motor_inferencia import generar_alertas

RUTA_MODELO = "Train_IA/artifacts/modelo_gru.keras"
RUTA_SCALER = "Train_IA/artifacts/scaler.pkl"


@st.cache_resource(show_spinner="Cargando modelo de IA...")
def _cargar_modelo_y_scaler():
    """
    Carga el modelo y el escalador UNA sola vez por sesión de Streamlit.
    Son artefactos pesados (el modelo son varias capas GRU); recargarlos
    en cada rerun haría la app muy lenta.
    """
    from tensorflow.keras.models import load_model

    modelo = load_model(RUTA_MODELO)
    scaler = joblib.load(RUTA_SCALER)
    return modelo, scaler


@st.cache_data(show_spinner="Generando pronóstico...", ttl=300)
def predecir_estado_futuro(df_historial):
    """
    df_historial: el DataFrame COMPLETO que devuelve utils/datos.cargar_datos()
    (columnas timestamp, temp_ambiente, hum_ambiente, hum_suelo, lluvia_pct),
    no solo la última fila -- el modelo necesita historial.

    Devuelve un diccionario con las alertas agronómicas y un resumen del
    pronóstico, o None si todavía no hay suficiente historial limpio.

    Cacheado 5 minutos: recalcular esto (limpieza + resampleo + predicción)
    en cada clic del usuario sería lento y no aporta nada, porque el
    historial no cambia tan rápido.
    """

    lookback = CONFIG_ENTRENAMIENTO["lookback_pasos"]
    pasos_lluvia = CONFIG_ENTRENAMIENTO["pasos_lluvia_reciente"]

    # 1. Limpieza -- el mismo pipeline usado para entrenar el modelo
    df_limpio = pipeline_limpieza_invernadero(df_historial.copy(), CONFIG)

    # 2. Resampleo a 15 min -- el modelo se entrenó a esta frecuencia
    df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO).dropna()

    if len(df_15min) < lookback:
        return None  # aún no hay ~48h de historial limpio y continuo

    ventana_reciente = df_15min.iloc[-lookback:]

    # 3. Escalar con el escalador YA AJUSTADO durante el entrenamiento
    modelo, scaler = _cargar_modelo_y_scaler()

    ventana_escalada = transformar_con_scaler_existente(
        ventana_reciente, scaler, CONFIG_ENTRENAMIENTO
    )

    columnas_features = (
        CONFIG_ENTRENAMIENTO["columnas_agregacion_media"]
        + CONFIG_ENTRENAMIENTO["columnas_agregacion_max"]
    )

    X = ventana_escalada[columnas_features].values
    X = np.expand_dims(X, axis=0)  # forma: (1, lookback, n_features)

    # 4. Predicción del modelo (próximas horas, cada 15 min)
    prediccion_escalada = modelo.predict(X, verbose=0)

    prediccion_real = revertir_escala_targets(
        prediccion_escalada, scaler, CONFIG_ENTRENAMIENTO
    )[0]  # forma: (horizon, n_targets)

    pred_temp = prediccion_real[:, 0]
    pred_hum_ambiente = prediccion_real[:, 1]
    pred_hum_suelo = prediccion_real[:, 2]

    # La lluvia NUNCA se predice (no es un target del modelo): usamos la
    # lluvia real más reciente que sí observamos, no una inventada.
    lluvia_reciente = ventana_reciente["lluvia_pct"].iloc[-pasos_lluvia:].values

    alertas = generar_alertas(
        pred_temp, pred_hum_ambiente, pred_hum_suelo,
        lluvia_reciente, CONFIG_ENTRENAMIENTO
    )

    return {
        "alertas": alertas,
        "pred_temp_promedio": float(pred_temp.mean()),
        "pred_temp_max": float(pred_temp.max()),
        "pred_hum_suelo_min": float(pred_hum_suelo.min()),
        "horas_pronosticadas": CONFIG_ENTRENAMIENTO["horizon_pasos"] * 15 / 60,
    }