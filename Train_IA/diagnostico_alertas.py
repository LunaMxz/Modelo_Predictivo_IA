# diagnostico_alertas.py

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


def main():
    print("Reconstruyendo datos hasta la particion de test...")
    df_crudo = cargar_desde_mysql()
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO)
    train, val, test = dividir_cronologico(df_15min, CONFIG_ENTRENAMIENTO)

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
    y_test_reales = revertir_escala_targets(
        y_test, scaler, CONFIG_ENTRENAMIENTO
    )

    u = CONFIG_ENTRENAMIENTO["umbrales_agronomicos"]
    porcentaje_horizonte_optimo = CONFIG_ENTRENAMIENTO["porcentaje_horizonte_optimo"]
    umbral_lluvia_significativa = CONFIG_ENTRENAMIENTO["umbral_lluvia_significativa"]
    temp_templada_min = CONFIG_ENTRENAMIENTO["temp_templada_min"]
    temp_templada_max = CONFIG_ENTRENAMIENTO["temp_templada_max"]
    pasos_sostenidos = CONFIG_ENTRENAMIENTO["pasos_sostenidos_hongos"]

    columnas_orden = (
        CONFIG_ENTRENAMIENTO["columnas_agregacion_media"]
        + CONFIG_ENTRENAMIENTO["columnas_agregacion_max"]
    )
    idx_lluvia = columnas_orden.index("lluvia_pct")
    pasos_lluvia = CONFIG_ENTRENAMIENTO["pasos_lluvia_reciente"]

    # Predicciones vs. valores reales de test: el modelo predice algo razonable? 
    print("\n" + "=" * 60)
    print("0) PREDICCION vs REAL -- rango fisico general")
    print("=" * 60)
    nombres = CONFIG_ENTRENAMIENTO["targets"]
    for i, nombre in enumerate(nombres):
        p = predicciones_reales[:, :, i]
        r = y_test_reales[:, :, i]
        print(f"{nombre}:")
        print(f"  PREDICHO  min={p.min():.2f} mean={p.mean():.2f} max={p.max():.2f} std={p.std():.3f}")
        print(f"  REAL      min={r.min():.2f} mean={r.mean():.2f} max={r.max():.2f} std={r.std():.3f}")

    #1. Crecimiento optimo 
    print("\n" + "=" * 60)
    print(f"1) CRECIMIENTO OPTIMO (umbral: {porcentaje_horizonte_optimo*100:.0f}% del horizonte)")
    print("=" * 60)
    pred_temp = predicciones_reales[:, :, 0]
    pred_hum_suelo = predicciones_reales[:, :, 2]
    temp_en_rango = (pred_temp >= u["temp_optima_min"]) & (pred_temp <= u["temp_optima_max"])
    suelo_en_rango = pred_hum_suelo >= u["hum_suelo_optima_min"]
    ambas = temp_en_rango & suelo_en_rango
    porcentaje_por_muestra = ambas.mean(axis=1)  # % del horizonte en rango, por muestra
    print(f"% de temp en rango (global): {temp_en_rango.mean()*100:.1f}%")
    print(f"% de suelo en rango (global): {suelo_en_rango.mean()*100:.1f}%")
    print(f"% del horizonte en rango (promedio, media entre muestras): {porcentaje_por_muestra.mean()*100:.1f}%")
    print(f"Mejor muestra (% horizonte en rango): {porcentaje_por_muestra.max()*100:.1f}%")
    print(f"Muestras que superan el umbral de {porcentaje_horizonte_optimo*100:.0f}%: "
          f"{(porcentaje_por_muestra >= porcentaje_horizonte_optimo).sum()}/{len(porcentaje_por_muestra)}")

    # Estres hidrico
    print("\n" + "=" * 60)
    print(f"2) ESTRES HIDRICO (umbral suelo critico: {u['hum_suelo_critica_sequia']}, "
          f"umbral lluvia significativa: {umbral_lluvia_significativa})")
    print("=" * 60)
    suelo_critico_por_muestra = (pred_hum_suelo < u["hum_suelo_critica_sequia"]).any(axis=1)
    print(f"Muestras con suelo critico en algun paso: {suelo_critico_por_muestra.sum()}/{len(suelo_critico_por_muestra)}")
    lluvia_max_por_muestra = X_test_crudo[:, -pasos_lluvia:, idx_lluvia].max(axis=1)
    print(f"lluvia_reciente -- min={lluvia_max_por_muestra.min():.2f} "
          f"mean={lluvia_max_por_muestra.mean():.2f} max={lluvia_max_por_muestra.max():.2f}")
    sin_lluvia_significativa = lluvia_max_por_muestra <= umbral_lluvia_significativa
    print(f"Muestras SIN lluvia significativa reciente: {sin_lluvia_significativa.sum()}/{len(sin_lluvia_significativa)}")
    combinado = suelo_critico_por_muestra & sin_lluvia_significativa
    print(f"Muestras que cumplirian estres_hidrico: {combinado.sum()}/{len(combinado)}")

    # Escudo fungico
    print("\n" + "=" * 60)
    print(f"3) ESCUDO FUNGICO (hum > {u['hum_ambiente_critica_hongos']}, "
          f"temp en [{temp_templada_min},{temp_templada_max}], "
          f"racha >= {pasos_sostenidos} pasos)")
    print("=" * 60)
    pred_hum_ambiente = predicciones_reales[:, :, 1]
    hum_favorable = pred_hum_ambiente > u["hum_ambiente_critica_hongos"]
    temp_favorable = (pred_temp >= temp_templada_min) & (pred_temp <= temp_templada_max)
    print(f"% pasos con humedad favorable a hongos (global): {hum_favorable.mean()*100:.1f}%")
    print(f"% pasos con temp favorable a hongos (global): {temp_favorable.mean()*100:.1f}%")
    condicion = hum_favorable & temp_favorable
    print(f"% pasos con ambas condiciones (global): {condicion.mean()*100:.1f}%")

    def racha_maxima(fila):
        actual = maxima = 0
        for v in fila:
            actual = actual + 1 if v else 0
            maxima = max(maxima, actual)
        return maxima

    rachas = np.array([racha_maxima(fila) for fila in condicion])
    print(f"Racha maxima consecutiva -- min={rachas.min()} mean={rachas.mean():.2f} max={rachas.max()}")
    print(f"Muestras que alcanzan racha >= {pasos_sostenidos}: {(rachas >= pasos_sostenidos).sum()}/{len(rachas)}")


if __name__ == "__main__":
    main()