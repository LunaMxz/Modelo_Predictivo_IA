# test_resampleo.py

"""ATENCION ESTE ARCHIVO ES GENERADO POR IA PARA REALIZAR PRUEBAS UNICAMENTE
 no afecta funcionalidades ni sirve para el flujo de trabajo"""


import os
import sys
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Le indicamos a Python que busque dentro de la carpeta Train_IA para la DB
sys.path.append(os.path.abspath("Train_IA"))

from conexionDB.carga_mysql import cargar_desde_mysql
from limpieza import pipeline_limpieza_invernadero
from config import CONFIG
from resampleo import resamplear_a_15min
from config_entrenamiento import CONFIG_ENTRENAMIENTO

print("[Prueba] Iniciando extracción de datos desde MariaDB...")
df_crudo = cargar_desde_mysql()

print("[Prueba] Ejecutando limpieza de la Fase 1...")
df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)

print("[Prueba] Ejecutando resampleo a 15 minutos...")
df_15min = resamplear_a_15min(df_limpio, CONFIG_ENTRENAMIENTO)

# =============================================================================
# 📊 NUEVO BLOQUE: PARTIZIÓN, ESCALADO Y GUARDADO DE ARTEFACTOS
# =============================================================================
print("\n[Prueba] Dividiendo el dataset de forma cronológica (70% / 15% / 15%)...")
total_filas = len(df_15min)
idx_train = int(total_filas * 0.70)
idx_val = int(total_filas * 0.85)

# Separación limpia
train = df_15min.iloc[:idx_train]
val = df_15min.iloc[idx_train:idx_val]
test = df_15min.iloc[idx_val:]

print("[Prueba] Ajustando MinMaxScaler con el set de entrenamiento...")
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(train) # El ajuste se calcula estrictamente con los datos de train

# Transformación independiente de los 3 bloques
train_esc = pd.DataFrame(scaler.transform(train), columns=train.columns)
val_esc = pd.DataFrame(scaler.transform(val), columns=val.columns)
test_esc = pd.DataFrame(scaler.transform(test), columns=test.columns)

print("[Prueba] Creando carpeta de artefactos y guardando el scaler.pkl...")
# Crea la carpeta 'artifacts' en la raíz si no existe
os.makedirs("artifacts", exist_ok=True)
with open("artifacts/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print("✅ ¡scaler.pkl guardado exitosamente en la carpeta artifacts/!")

# =============================================================================
# 📉 PRUEBA DE CONTROL DE RANGOS
# =============================================================================
print("\n" + "="*50)
print("📈 RANGOS DE VALIDACIÓN ESCALADOS (val_esc)")
print("="*50)
print(val_esc.agg(["min", "max"]))

print("\n" + "="*50)
print("📈 RANGOS DE PRUEBA ESCALADOS (test_esc)")
print("="*50)
print(test_esc.agg(["min", "max"]))
print("="*50)

print(f"\n[Resumen] Train: {len(train_esc)} filas | Val: {len(val_esc)} filas | Test: {len(test_esc)} filas")