import streamlit as st
import pandas as pd

from utils.reglas_cultivo import UMBRALES


def mostrar_alertas(df):

    st.subheader("🚨 Centro de Alertas")

    # Búsqueda vectorizada (nada de .iterrows(), que con cientos de
    # miles de filas sería muy lento) y con los mismos umbrales que
    # usa el resto de la app (utils/reglas_cultivo.py), para no tener
    # un tercer juego de números distinto por ahí.

    u = UMBRALES

    temp_alta = df[df["temp_ambiente"] > u["temp_alta"]]
    suelo_bajo = df[df["hum_suelo"] < u["hum_suelo_baja"]]
    lluvia_alta = df[df["lluvia_pct"] > u["lluvia_alta"]]

    partes = []

    if len(temp_alta) > 0:
        parte = temp_alta[["timestamp", "temp_ambiente"]].copy()
        parte["Tipo"] = "🌡 Temperatura Alta"
        parte["Nivel"] = "Alta"
        parte = parte.rename(columns={"timestamp": "Fecha", "temp_ambiente": "Valor"})
        partes.append(parte[["Fecha", "Tipo", "Valor", "Nivel"]])

    if len(suelo_bajo) > 0:
        parte = suelo_bajo[["timestamp", "hum_suelo"]].copy()
        parte["Tipo"] = "🌱 Humedad Baja"
        parte["Nivel"] = "Media"
        parte = parte.rename(columns={"timestamp": "Fecha", "hum_suelo": "Valor"})
        partes.append(parte[["Fecha", "Tipo", "Valor", "Nivel"]])

    if len(lluvia_alta) > 0:
        parte = lluvia_alta[["timestamp", "lluvia_pct"]].copy()
        parte["Tipo"] = "🌧 Lluvia Elevada"
        parte["Nivel"] = "Baja"
        parte = parte.rename(columns={"timestamp": "Fecha", "lluvia_pct": "Valor"})
        partes.append(parte[["Fecha", "Tipo", "Valor", "Nivel"]])

    if not partes:

        st.success("✅ No existen alertas registradas en el rango seleccionado.")

    else:

        tabla = pd.concat(partes).sort_values("Fecha", ascending=False)

        st.caption(f"{len(tabla)} alertas encontradas en el rango seleccionado.")

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

    st.divider()