import streamlit as st
import pandas as pd
from datetime import timedelta


def mostrar_filtros(df):

    st.sidebar.header("🎛️ Filtros")

    # Convertimos la fecha a formato datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fecha_maxima = df["timestamp"].max().date()
    fecha_minima_disponible = df["timestamp"].min().date()

    # Por defecto mostramos solo los últimos 2 días, no el historial
    # completo -- con cientos de miles de filas, graficar todo el rango
    # de una vez puede congelar el navegador. El usuario puede ampliarlo
    # si de verdad lo necesita.
    fecha_inicio_default = max(
        fecha_minima_disponible,
        fecha_maxima - timedelta(days=2)
    )

    fecha_inicio = st.sidebar.date_input(
        "Fecha inicial",
        value=fecha_inicio_default,
        min_value=fecha_minima_disponible,
        max_value=fecha_maxima,
    )

    fecha_fin = st.sidebar.date_input(
        "Fecha final",
        value=fecha_maxima,
        min_value=fecha_minima_disponible,
        max_value=fecha_maxima,
    )

    if (fecha_fin - fecha_inicio).days > 7:
        st.sidebar.warning(
            "Rangos mayores a 7 días pueden tardar más en cargar."
        )

    df_filtrado = df[
        (df["timestamp"].dt.date >= fecha_inicio) &
        (df["timestamp"].dt.date <= fecha_fin)
    ]

    return df_filtrado