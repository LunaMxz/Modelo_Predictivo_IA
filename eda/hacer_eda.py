"""
hacer_eda.py
Analisis Exploratorio de Datos (EDA): genera 3 graficos a partir de
datos_eda.csv para entender las variables antes de entrenar la IA.

Este archivo vive en la carpeta eda/. El truco de abajo encuentra la
carpeta del proyecto sola, asi funciona lo ejecutes desde donde lo ejecutes.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Leer y guardar TODO dentro de esta misma carpeta eda/resultados ---
AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(AQUI, "resultados")

# Cargar los datos generados
ruta_csv = os.path.join(CARPETA, "datos_eda.csv")
df = pd.read_csv(ruta_csv, parse_dates=["timestamp"])

variables = ["temp_ambiente", "hum_ambiente", "hum_suelo", "lluvia_pct"]
colores = ["#D85A30", "#1D9E75", "#378ADD", "#534AB7"]
titulos = ["Temperatura (°C)", "Humedad aire (%)", "Humedad suelo (%)", "Lluvia (%)"]

# ===== GRAFICO 1: Lineas en el tiempo =====
fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True)
for ax, var, c, t in zip(axes, variables, colores, titulos):
    ax.plot(df["timestamp"], df[var], color=c, linewidth=1)
    ax.set_ylabel(t, fontsize=9)
    ax.grid(alpha=0.3)
axes[0].set_title("Evolucion de las variables en el tiempo", fontsize=13, weight="bold")
axes[-1].set_xlabel("Fecha")
plt.tight_layout()
plt.savefig(os.path.join(CARPETA, "eda_1_lineas.png"), dpi=90)
plt.close()

# ===== GRAFICO 2: Histogramas =====
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
for ax, var, c, t in zip(axes.flat, variables, colores, titulos):
    ax.hist(df[var], bins=25, color=c, alpha=0.75, edgecolor="white")
    ax.set_title(t, fontsize=10)
    ax.grid(alpha=0.3)
fig.suptitle("Distribucion de cada variable", fontsize=13, weight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CARPETA, "eda_2_histogramas.png"), dpi=90)
plt.close()

# ===== GRAFICO 3: Correlacion =====
plt.figure(figsize=(7, 6))
corr = df[variables].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f",
            square=True, linewidths=1)
plt.title("Correlacion entre variables", fontsize=13, weight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CARPETA, "eda_3_correlacion.png"), dpi=90)
plt.close()

print(f"3 graficos guardados en: {CARPETA}")
print("\nTabla de correlacion:")
print(corr.round(2).to_string())