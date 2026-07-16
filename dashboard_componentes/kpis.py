import streamlit as st


def mostrar_kpis(df):

    st.subheader("📊 Estado Actual de los Sensores")

    c1, c2, c3, c4 = st.columns(4)

    # -----------------------------
    # Temperatura
    # -----------------------------
    with c1:

        with st.container(border=True):

            st.markdown("### 🌡 Temperatura")

            st.metric(
                label="Actual",
                value=f"{df['temp_ambiente'].iloc[-1]:.1f} °C",
                delta=f"{df['temp_ambiente'].iloc[-1]-df['temp_ambiente'].iloc[-2]:.1f} °C"
            )

            st.caption(
                f"Promedio: {df['temp_ambiente'].mean():.1f} °C"
            )

    # -----------------------------
    # Humedad Ambiente
    # -----------------------------
    with c2:

        with st.container(border=True):

            st.markdown("### 💧 Humedad")

            st.metric(

                label="Actual",

                value=f"{df['hum_ambiente'].iloc[-1]:.1f} %",

                delta=f"{df['hum_ambiente'].iloc[-1]-df['hum_ambiente'].iloc[-2]:.1f} %"

            )

            st.caption(

                f"Promedio: {df['hum_ambiente'].mean():.1f} %"

            )

    # -----------------------------
    # Humedad Suelo
    # -----------------------------
    with c3:

        with st.container(border=True):

            st.markdown("### 🌱 Humedad Suelo")

            st.metric(

                label="Actual",

                value=f"{df['hum_suelo'].iloc[-1]:.1f} %",

                delta=f"{df['hum_suelo'].iloc[-1]-df['hum_suelo'].iloc[-2]:.1f} %"

            )

            st.caption(

                f"Promedio: {df['hum_suelo'].mean():.1f} %"

            )

    # -----------------------------
    # Lluvia
    # -----------------------------
    with c4:

        with st.container(border=True):

            st.markdown("### 🌧 Lluvia")

            st.metric(

                label="Actual",

                value=f"{df['lluvia_pct'].iloc[-1]:.1f} %",

                delta=f"{df['lluvia_pct'].iloc[-1]-df['lluvia_pct'].iloc[-2]:.1f} %"

            )

            st.caption(

                f"Máxima: {df['lluvia_pct'].max():.1f} %"

            )

    st.divider()