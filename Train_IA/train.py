# train.py
import sys
import os


RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(RAIZ_PROYECTO)

from config import CONFIG
from limpieza import pipeline_limpieza_invernadero
from conexionDB.carga_mysql import cargar_desde_mysql

from config_entrenamiento import CONFIG_ENTRENAMIENTO
from resampleo import resamplear_a_15min
from particion import dividir_cronologico
from escalador import ajustar_y_transformar
from ventaneo import crear_ventanas
from modelo_gru import construir_modelo_gru
from entrenamiento import entrenar_modelo

def main():
    print("_" * 60)
    print("[TRAIN] Paso 1: Cargando datos reales desde MariaDB...")
    print("_" * 60)
    df_crudo = cargar_desde_mysql()
    print(f"Registros cargados: {len(df_crudo)}")

    print("\n" + "_" * 60)
    print("[TRAIN] Paso 2: Pipeline de limpieza")
    print("_" * 60)
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    print(f"Registros tras limpieza: {len(df_limpio)}")

    #resampleo
    print("\n" + "_" * 60)
    print("[TRAIN] Paso 2.5: Resampleo 15s -> 15min")
    print("_" * 60)
    df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO)
    print(f"Filas tras resampleo: {len(df_15min)}")
    print(f"NaNs por columna:\n{df_15min.isna().sum()}")

    # particion cronologica 70/15/15
    print("\n" + "_" * 60)
    print("[TRAIN] Paso 2.6: Particion cronologica")
    print("_" * 60)
    train, val, test = dividir_cronologico(df_15min, CONFIG_ENTRENAMIENTO)

    # ajuste del escalador (solo con train)
    print("\n" + "_" * 60)
    print("[TRAIN] Paso 3: Ajuste del escalador")
    print("_" * 60)
    train_esc, val_esc, test_esc, scaler = ajustar_y_transformar(
        train, val, test, CONFIG_ENTRENAMIENTO
    )

    # ventaneo (tensores 3D, aislamiento estricto)
    print("\n" + "_" * 60)
    print("[TRAIN] Paso 4-5: Construccion de ventanas (X, y)")
    print("_" * 60)
    X_train, y_train = crear_ventanas(train_esc, CONFIG_ENTRENAMIENTO)
    X_val, y_val = crear_ventanas(val_esc, CONFIG_ENTRENAMIENTO)
    X_test, y_test = crear_ventanas(test_esc, CONFIG_ENTRENAMIENTO)
    print(f"X_train: {X_train.shape}  y_train: {y_train.shape}")
    print(f"X_val:   {X_val.shape}  y_val:   {y_val.shape}")
    print(f"X_test:  {X_test.shape}  y_test:  {y_test.shape}")

    # arquitectura GRU
    print("\n" + "_" * 60)
    print("[TRAIN] Paso 6: Construccion de la arquitectura GRU")
    print("_" * 60)
    modelo = construir_modelo_gru(CONFIG_ENTRENAMIENTO)
    modelo.summary()

    #entrenamiento real
    print("\n" + "_" * 60)
    print("[TRAIN] Paso 7: Entrenamiento")
    print("_" * 60)
    historia = entrenar_modelo(modelo, X_train, y_train, X_val, y_val)

    return modelo, historia, (X_test, y_test)

if __name__ == "__main__":
    main()
