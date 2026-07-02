import streamlit as st
import pandas as pd

# Cargar datos
df = pd.read_csv("data/procesado/datos_limpios.csv")

st.title(" Dashboard de Salud del Cultivo")


# KPIs
st.subheader(" Indicadores generales")

col1, col2, col3 = st.columns(3)

col1.metric(" Temp promedio", round(df["temp_ambiente"].mean(), 2))
col2.metric(" Humedad ambiente", round(df["hum_ambiente"].mean(), 2))
col3.metric(" Lluvia max", round(df["lluvia_pct"].max(), 2))


# Gráficas

st.subheader(" Evolución de sensores")

st.line_chart(df.set_index("timestamp")[["temp_ambiente"]])
st.line_chart(df.set_index("timestamp")[["hum_ambiente"]])
st.line_chart(df.set_index("timestamp")[["hum_suelo"]])
st.line_chart(df.set_index("timestamp")[["lluvia_pct"]])


# Alertas simples

st.subheader(" Detección de estrés")

if df["temp_ambiente"].max() > 35:
    st.error("Estrés térmico detectado")
else:
    st.success("Sin estrés térmico")

if df["hum_suelo"].mean() < 30:
    st.warning("Posible estrés hídrico")