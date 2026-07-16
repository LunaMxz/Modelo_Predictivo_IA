import streamlit as st


def mostrar_resumen(df):

    ultimo = df.iloc[-1]

    st.markdown("## 📅 Última actualización")

    col1, col2 = st.columns([1, 2])

    with col1:

        st.metric(
            "🌡 Temperatura",
            f"{float(ultimo['temp_ambiente']):.1f} °C"
        )

        st.metric(
            "💧 Humedad ambiente",
            f"{float(ultimo['hum_ambiente']):.1f} %"
        )

    with col2:

        st.metric(
            "🌱 Humedad del suelo",
            f"{float(ultimo['hum_suelo']):.1f} %"
        )

        st.metric(
            "🌧 Lluvia",
            f"{float(ultimo['lluvia_pct']):.1f} %"
        )

    st.info(
        f"🕒 Última lectura registrada: **{ultimo['timestamp']}**"
    )

    st.divider()