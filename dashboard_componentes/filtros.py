import streamlit as st
import pandas as pd


def mostrar_filtros(df):

    st.sidebar.header("🎛️ Filtros")

    # Convertimos la fecha a formato datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fecha_inicio = st.sidebar.date_input(
        "Fecha inicial",
        value=df["timestamp"].min().date()
    )

    fecha_fin = st.sidebar.date_input(
        "Fecha final",
        value=df["timestamp"].max().date()
    )

    df_filtrado = df[
        (df["timestamp"].dt.date >= fecha_inicio) &
        (df["timestamp"].dt.date <= fecha_fin)
    ]

    return df_filtrado