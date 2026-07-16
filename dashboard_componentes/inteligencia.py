import streamlit as st
import plotly.graph_objects as go

from utils.reglas_cultivo import evaluar_estado


def mostrar_inteligencia(df):

    st.subheader("🔎 Diagnóstico del cultivo")

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

    # ======================================
    # Gauge de riesgo (mismo cálculo que el resto del dashboard)
    # ======================================

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=estado["riesgo_pct"],

        number={"suffix": "%"},

        title={"text": "Nivel de Riesgo"},

        gauge={

            "axis": {"range": [0, 100]},

            "bar": {"color": "darkblue"},

            "steps": [

                {"range": [0, 40], "color": "green"},

                {"range": [40, 70], "color": "gold"},

                {"range": [70, 100], "color": "red"}

            ]
        }

    ))

    col1, col2 = st.columns([2, 1])

    with col1:

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.metric(
            "Estado",
            f"{estado['icono']} {estado['titulo']}"
        )

        st.info(estado["mensaje"])

    st.divider()

    # ======================================
    # Recomendación
    # ======================================

    st.subheader("💡 Qué hacer ahora")

    if estado["nivel"] == "critico":
        st.error(f"👉 {estado['accion']}")
    elif estado["nivel"] == "atencion":
        st.warning(f"👉 {estado['accion']}")
    else:
        st.success(f"👉 {estado['accion']}")

    st.divider()