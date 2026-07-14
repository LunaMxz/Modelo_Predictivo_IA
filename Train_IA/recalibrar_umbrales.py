# recalibrar_umbrales.py

import sys
import os
import numpy as np

RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(RAIZ_PROYECTO)

from config import CONFIG
from limpieza import pipeline_limpieza_invernadero
from conexionDB.carga_mysql import cargar_desde_mysql
from config_entrenamiento import CONFIG_ENTRENAMIENTO
from resampleo import resamplear_a_15min
from particion import dividir_cronologico


def main():
    df_crudo = cargar_desde_mysql()
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO)
    train, val, test = dividir_cronologico(df_15min, CONFIG_ENTRENAMIENTO)

    u = CONFIG_ENTRENAMIENTO["umbrales_agronomicos"]

    print("=" * 60)
    print("RANGO REAL (crudo, sin escalar) -- solo particion TRAIN")
    print("=" * 60)

    for col, umbral_bajo, umbral_alto in [
        ("temp_ambiente", "temp_optima_min", "temp_critica_calor"),
        ("hum_ambiente", None, "hum_ambiente_critica_hongos"),
        ("hum_suelo", "hum_suelo_critica_sequia", "hum_suelo_optima_min"),
    ]:
        serie = train[col]
        print(f"\n{col}: min={serie.min():.2f}  p10={serie.quantile(0.10):.2f}  "
              f"p25={serie.quantile(0.25):.2f}  mean={serie.mean():.2f}  "
              f"p90={serie.quantile(0.90):.2f}  max={serie.max():.2f}")
        if umbral_bajo:
            print(f"  umbral actual '{umbral_bajo}': {u[umbral_bajo]}")
        if umbral_alto:
            print(f"  umbral actual '{umbral_alto}': {u[umbral_alto]}")

    print("\n" + "=" * 60)
    print("UMBRALES RECALIBRADOS SUGERIDOS (basados en percentiles de TU train)")
    print("=" * 60)
    print("Regla: p10 = condicion baja poco comun (sequia real), "
          "p90 = condicion alta poco comun (saturacion real).")
    print(f'"hum_suelo_critica_sequia": {train["hum_suelo"].quantile(0.25):.1f},  '
          f'# antes: {u["hum_suelo_critica_sequia"]}')
    print(f'"hum_suelo_optima_min": {train["hum_suelo"].quantile(0.25):.1f},  '
          f'# antes: {u["hum_suelo_optima_min"]}')
    print(f'"hum_ambiente_critica_hongos": {train["hum_ambiente"].quantile(0.90):.1f},  '
          f'# antes: {u["hum_ambiente_critica_hongos"]}')


if __name__ == "__main__":
    main()