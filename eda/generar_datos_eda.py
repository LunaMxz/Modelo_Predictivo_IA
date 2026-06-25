"""
generar_datos_eda.py
Genera ~500 lecturas sinteticas REALISTAS de los sensores para el EDA.
Simula varios dias con ciclo dia/noche y eventos de lluvia.

Este archivo vive en la carpeta eda/. El truco de abajo encuentra la
carpeta del proyecto sola, asi funciona lo ejecutes desde donde lo ejecutes.
"""
import os
import numpy as np
import pandas as pd

# --- Guardar TODO dentro de esta misma carpeta eda/resultados ---
# AQUI = la carpeta donde vive este archivo (eda/)
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "resultados")
os.makedirs(SALIDA, exist_ok=True)  # crea la carpeta si no existe

# Para que los datos sean iguales cada vez que corres (reproducible)
np.random.seed(42)

# 1. Crear fechas: 500 lecturas, una cada 30 minutos
n = 500
fechas = pd.date_range(start="2026-06-01 00:00:00", periods=n, freq="30min")

# 2. La "hora del dia" nos sirve para simular dia y noche
hora = fechas.hour + fechas.minute / 60

# 3. TEMPERATURA: sube de dia, baja de noche (onda) + ruido
temp = 24 + 6 * np.sin((hora - 9) / 24 * 2 * np.pi) + np.random.normal(0, 0.8, n)

# 4. HUMEDAD DEL AIRE: al reves de la temperatura (mas humedo de noche)
hum_aire = 70 - 1.8 * (temp - 24) + np.random.normal(0, 3, n)
hum_aire = np.clip(hum_aire, 30, 95)

# 5. LLUVIA: casi siempre 0, con algunos eventos al azar
lluvia = np.zeros(n)
eventos = np.random.choice(range(n), size=15, replace=False)
for e in eventos:
    lluvia[e] = np.random.uniform(40, 100)

# 6. HUMEDAD DEL SUELO: baja al secarse y SUBE despues de llover
suelo = np.zeros(n)
suelo[0] = 55
for i in range(1, n):
    if lluvia[i] > 0:
        suelo[i] = min(suelo[i-1] + lluvia[i] * 0.15, 80)
    else:
        suelo[i] = max(suelo[i-1] - 0.25, 25)

# 7. Armar la tabla
df = pd.DataFrame({
    "timestamp": fechas,
    "temp_ambiente": temp.round(1),
    "hum_ambiente": hum_aire.round(1),
    "hum_suelo": suelo.round(1),
    "lluvia_pct": lluvia.round(1),
})

# 8. Guardar
ruta_csv = os.path.join(SALIDA, "datos_eda.csv")
df.to_csv(ruta_csv, index=False)
print(f"Generadas {len(df)} lecturas. Guardado en: {ruta_csv}")
print(df.head(10).to_string(index=False))