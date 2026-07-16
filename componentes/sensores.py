import streamlit as st


def mostrar_sensores(df):

    # Últimos valores
    temperatura = float(df["temp_ambiente"].iloc[-1])
    humedad_ambiente = float(df["hum_ambiente"].iloc[-1])
    humedad_suelo = float(df["hum_suelo"].iloc[-1])
    lluvia = float(df["lluvia_pct"].iloc[-1])

    st.subheader("🌿 Estado de los sensores")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🌡 Temperatura",
            value=f"{temperatura:.1f} °C"
        )

    with col2:
        st.metric(
            label="💧 Humedad ambiente",
            value=f"{humedad_ambiente:.1f} %"
        )

    with col3:
        st.metric(
            label="🌱 Humedad del suelo",
            value=f"{humedad_suelo:.1f} %"
        )

    with col4:
        st.metric(
            label="🌧 Lluvia",
            value=f"{lluvia:.1f} %"
        )

    st.divider()