import streamlit as st


def seleccionar_sensor(df):

    if "sensor" not in st.session_state:
        st.session_state.sensor = "temp_ambiente"

    st.markdown("## 📊 Sensores")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            f"🌡\n\n{df['temp_ambiente'].iloc[-1]:.1f} °C",
            use_container_width=True
        ):
            st.session_state.sensor = "temp_ambiente"

    with col2:

        if st.button(
            f"💧\n\n{df['hum_ambiente'].iloc[-1]:.1f} %",
            use_container_width=True
        ):
            st.session_state.sensor = "hum_ambiente"

    with col3:

        if st.button(
            f"🌱\n\n{df['hum_suelo'].iloc[-1]:.1f} %",
            use_container_width=True
        ):
            st.session_state.sensor = "hum_suelo"

    with col4:

        if st.button(
            f"🌧\n\n{df['lluvia_pct'].iloc[-1]:.1f} %",
            use_container_width=True
        ):
            st.session_state.sensor = "lluvia_pct"

    nombres = {

        "temp_ambiente": "Temperatura Ambiente",

        "hum_ambiente": "Humedad Ambiente",

        "hum_suelo": "Humedad del Suelo",

        "lluvia_pct": "Porcentaje de Lluvia"

    }

    return st.session_state.sensor, nombres[st.session_state.sensor]