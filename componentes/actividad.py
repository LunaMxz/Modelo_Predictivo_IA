import streamlit as st


def mostrar_actividad(df):

    temperatura = float(df["temp_ambiente"].iloc[-1])
    humedad = float(df["hum_suelo"].iloc[-1])
    lluvia = float(df["lluvia_pct"].iloc[-1])

    st.subheader("📋 Actividad reciente")

    actividades = []

    actividades.append((
        "🛰️",
        "Sensores sincronizados",
        "Los sensores enviaron correctamente la última lectura."
    ))

    if temperatura > 30:

        actividades.append((
            "🌡️",
            "Temperatura elevada",
            "Conviene aumentar la ventilación del invernadero."
        ))

    else:

        actividades.append((
            "🌡️",
            "Temperatura adecuada",
            "La temperatura permanece dentro del rango recomendado."
        ))

    if humedad < 40:

        actividades.append((
            "💧",
            "Suelo con poca humedad",
            "Es recomendable revisar el sistema de riego."
        ))

    else:

        actividades.append((
            "🌱",
            "Suelo saludable",
            "La humedad del suelo es adecuada para el cultivo."
        ))

    if lluvia > 50:

        actividades.append((
            "🌧️",
            "Presencia de lluvia",
            "Se detectó un nivel alto de precipitación."
        ))

    actividades.append((
        "🤖",
        "Análisis actualizado",
        "La inteligencia artificial revisó el estado actual del cultivo."
    ))

    for icono, titulo, descripcion in actividades:

        with st.container(border=True):

            st.markdown(f"### {icono} {titulo}")

            st.write(descripcion)

    st.divider()