import streamlit as st

from utils.reglas_cultivo import evaluar_estado


def mostrar_recomendacion(df):

    temperatura = float(df["temp_ambiente"].iloc[-1])
    humedad_suelo = float(df["hum_suelo"].iloc[-1])
    humedad_ambiente = float(df["hum_ambiente"].iloc[-1]) if "hum_ambiente" in df else None
    lluvia = float(df["lluvia_pct"].iloc[-1]) if "lluvia_pct" in df else None

    estado = evaluar_estado(
        temperatura,
        humedad_suelo,
        humedad_ambiente,
        lluvia,
    )

    st.subheader("💡 Recomendación")

    texto = f"### {estado['icono']} {estado['titulo']}\n\n{estado['mensaje']}\n\n👉 **{estado['accion']}**"

    if estado["nivel"] == "critico":
        st.error(texto)
    elif estado["nivel"] == "atencion":
        st.warning(texto)
    else:
        st.success(texto)

    st.divider()