# train.py
import sys
import os


RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(RAIZ_PROYECTO)

from config import CONFIG
from limpieza import pipeline_limpieza_invernadero
from conexionDB.carga_mysql import cargar_desde_mysql


def main():
    print("[TRAIN] Cargando datos reales desde MariaDB...")
    df_crudo = cargar_desde_mysql()
    print(f"[TRAIN] Registros cargados: {len(df_crudo)}")

    print("[TRAIN] Corriendo pipeline de limpieza...")
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    print(f"[TRAIN] Registros tras limpieza: {len(df_limpio)}")



if __name__ == "__main__":
    main()

   