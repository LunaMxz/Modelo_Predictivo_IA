# diagnostico_final.py
"""
Descompone cada alerta en sus condiciones individuales para encontrar
EXACTAMENTE cual pieza esta bloqueando cada una. Reutiliza las mismas
predicciones que analisis_alertas.py, sin volver a entrenar.
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
from evaluacion import revertir_escala_targets
from motor_inferencia import _hay_racha_sostenida


def main():
    df_crudo = cargar_desde_mysql()
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO)
    _, _, test = dividir_cronologico(df_15min, CONFIG_ENTRENAMIENTO)

    scaler = joblib.load("artifacts/scaler.pkl")
    test_esc = transformar_con_scaler_existente(test, scaler, CONFIG_ENTRENAMIENTO)
    X_test, y_test = crear_ventanas(test_esc, CONFIG_ENTRENAMIENTO)
    X_test_crudo, _ = crear_ventanas(test, CONFIG_ENTRENAMIENTO)

    modelo = load_model("artifacts/modelo_gru.keras")
    pred_esc = modelo.predict(X_test, verbose=0)
    pred_real = revertir_escala_targets(pred_esc, scaler, CONFIG_ENTRENAMIENTO)

    u = CONFIG_ENTRENAMIENTO["umbrales_agronomicos"]
    columnas_orden = (CONFIG_ENTRENAMIENTO["columnas_agregacion_media"]
                       + CONFIG_ENTRENAMIENTO["columnas_agregacion_max"])
    idx_lluvia = columnas_orden.index("lluvia_pct")
    pasos_lluvia = CONFIG_ENTRENAMIENTO["pasos_lluvia_reciente"]
    pasos_sostenidos = CONFIG_ENTRENAMIENTO["pasos_sostenidos_hongos"]
    n = pred_real.shape[0]

    print("=" * 60)
    print("CRECIMIENTO OPTIMO -- por que falla")
    print("=" * 60)
    temp_ok_todo_horizonte = 0
    suelo_ok_todo_horizonte = 0
    ambos_ok = 0
    for i in range(n):
        temp_ok = np.all((pred_real[i,:,0] >= u["temp_optima_min"]) & (pred_real[i,:,0] <= u["temp_optima_max"]))
        suelo_ok = np.all(pred_real[i,:,2] >= u["hum_suelo_optima_min"])
        temp_ok_todo_horizonte += temp_ok
        suelo_ok_todo_horizonte += suelo_ok
        ambos_ok += (temp_ok and suelo_ok)
    print(f"Muestras donde TEMP se mantiene en rango los 48 pasos: {temp_ok_todo_horizonte}/{n}")
    print(f"Muestras donde SUELO se mantiene en rango los 48 pasos: {suelo_ok_todo_horizonte}/{n}")
    print(f"Muestras donde AMBOS se cumplen (esto es el resultado final): {ambos_ok}/{n}")

    print("\n" + "=" * 60)
    print("ESTRES HIDRICO -- por que falla")
    print("=" * 60)
    suelo_critico_count = 0
    hubo_lluvia_count = 0
    ambos_count = 0
    for i in range(n):
        suelo_critico = np.any(pred_real[i,:,2] < u["hum_suelo_critica_sequia"])
        lluvia_reciente = X_test_crudo[i, -pasos_lluvia:, idx_lluvia]
        hubo_lluvia = np.max(lluvia_reciente) > 0
        suelo_critico_count += suelo_critico
        hubo_lluvia_count += hubo_lluvia
        ambos_count += (suelo_critico and not hubo_lluvia)
    print(f"Muestras donde SUELO cruza umbral de sequia (sin importar lluvia): {suelo_critico_count}/{n}")
    print(f"Muestras donde HUBO lluvia reciente (esto SUPRIME la alerta): {hubo_lluvia_count}/{n}")
    print(f"Muestras donde se activa la alerta final (suelo critico Y sin lluvia): {ambos_count}/{n}")

    print("\n" + "=" * 60)
    print("ESCUDO FUNGICO -- por que falla")
    print("=" * 60)
    algun_paso_favorable_count = 0
    racha_maxima_global = 0
    con_racha_suficiente = 0
    for i in range(n):
        hum_fav = pred_real[i,:,1] > u["hum_ambiente_critica_hongos"]
        temp_fav = (pred_real[i,:,0] >= u["temp_optima_min"]) & (pred_real[i,:,0] <= u["temp_optima_max"])
        combinada = hum_fav & temp_fav
        if np.any(combinada):
            algun_paso_favorable_count += 1
        # calcular racha maxima de esta muestra
        racha_actual = 0
        racha_maxima_muestra = 0
        for v in combinada:
            racha_actual = racha_actual + 1 if v else 0
            racha_maxima_muestra = max(racha_maxima_muestra, racha_actual)
        racha_maxima_global = max(racha_maxima_global, racha_maxima_muestra)
        if _hay_racha_sostenida(combinada, pasos_sostenidos):
            con_racha_suficiente += 1
    print(f"Muestras con AL MENOS 1 paso favorable a hongos (humedad+temp simultaneas): {algun_paso_favorable_count}/{n}")
    print(f"Racha consecutiva mas larga encontrada en TODO test: {racha_maxima_global} pasos "
          f"(se necesitan {pasos_sostenidos} para disparar la alerta)")
    print(f"Muestras con racha suficiente (esto es el resultado final): {con_racha_suficiente}/{n}")


if __name__ == "__main__":
    main()
