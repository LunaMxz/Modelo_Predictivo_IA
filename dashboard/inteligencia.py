import streamlit as st
import plotly.graph_objects as go


def mostrar_inteligencia(df):

    st.subheader("🤖 Inteligencia Artificial")

    temperatura = df["temp_ambiente"].iloc[-1]
    humedad = df["hum_suelo"].iloc[-1]

    # ======================================
    # Simulación del modelo IA
    # ======================================

    def predecir_riesgo(temp, hum):

        if temp > 30 and hum < 35:
            return 90

        elif temp > 28 or hum < 40:
            return 60

        else:
            return 15

    riesgo = predecir_riesgo(
        temperatura,
        humedad
    )

    confianza = 96.4

    # ======================================
    # Gauge
    # ======================================

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=riesgo,

        number={"suffix":"%"},

        title={"text":"Nivel de Riesgo"},

        gauge={

            "axis":{"range":[0,100]},

            "bar":{"color":"darkblue"},

            "steps":[

                {"range":[0,40],"color":"green"},

                {"range":[40,70],"color":"gold"},

                {"range":[70,100],"color":"red"}

            ]
        }

    ))

    col1, col2 = st.columns([2,1])

    with col1:

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        if riesgo >= 80:

            estado = "🔴 Riesgo Alto"

            prediccion = "Alta probabilidad de estrés hídrico."

        elif riesgo >= 50:

            estado = "🟡 Riesgo Medio"

            prediccion = "Posible inicio de estrés."

        else:

            estado = "🟢 Riesgo Bajo"

            prediccion = "Cultivo estable."

        st.metric(
            "Estado",
            estado
        )

        st.metric(
            "Confianza del modelo",
            f"{confianza:.1f}%"
        )

        st.info(prediccion)

    st.divider()

    # ======================================
    # Recomendación
    # ======================================

    st.subheader("💡 Recomendación Inteligente")

    if riesgo >= 80:

        st.error("""
• Activar ventilación.

• Incrementar riego.

• Revisar el cultivo inmediatamente.
""")

    elif riesgo >= 50:

        st.warning("""
• Supervisar la temperatura.

• Revisar humedad del suelo.

• Continuar monitoreo.
""")

    else:

        st.success("""
El cultivo presenta condiciones normales.

No se requieren acciones correctivas.
""")

    st.divider()