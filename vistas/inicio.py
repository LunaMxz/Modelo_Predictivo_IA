import streamlit as st

def mostrar_inicio(df):

    st.title("🌱 Agroindustria")

    st.caption("Sistema Inteligente de Monitoreo para Invernaderos")

    st.markdown("---")

    # ==========================
    # ESTADO DEL CULTIVO
    # ==========================

    st.header("🟢 Estado del cultivo")

    ultima_actualizacion = df["timestamp"].iloc[-1]
    st.caption(f"🕒 Última actualización: {ultima_actualizacion}")

    temperatura = df["temp_ambiente"].iloc[-1]
    humedad = df["hum_suelo"].iloc[-1]

    if 22 <= temperatura <= 28 and humedad >= 40:
        st.success("🟢 El cultivo está en buenas condiciones.")

    elif temperatura > 30:
        st.warning("🟡 Temperatura elevada. Se recomienda revisar el sistema de ventilación.")

    else:
        st.error("🔴 El cultivo requiere atención.")

    st.write("""
Desde aquí podrás consultar en tiempo real el estado de tu cultivo,
visualizar los sensores y recibir alertas cuando exista algún problema.
""")

    st.markdown("---")

    # ==========================
    # TARJETAS
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌡 Temperatura",
            f"{df['temp_ambiente'].iloc[-1]:.1f} °C"
        )

    with col2:
        st.metric(
            "💧 Humedad ambiente",
            f"{df['hum_ambiente'].iloc[-1]:.1f} %"
        )

    with col3:
        st.metric(
            "🌱 Humedad del suelo",
            f"{df['hum_suelo'].iloc[-1]:.1f} %"
        )

    with col4:
        st.metric(
            "🌧 Lluvia",
            f"{df['lluvia_pct'].iloc[-1]:.1f} %"
        )

    st.markdown("---")

    st.subheader("📈 Comportamiento del cultivo")

    st.line_chart(
        df.set_index("timestamp")[
            [
                "temp_ambiente",
                "hum_ambiente"
            ]
        ]
    )

    st.markdown("---")

    st.subheader("📋 Últimos registros")

    tabla = df.tail(10).rename(columns={
        "timestamp": "Fecha",
        "temp_ambiente": "Temperatura (°C)",
        "hum_ambiente": "Humedad ambiente (%)",
        "hum_suelo": "Humedad del suelo (%)",
        "lluvia_pct": "Lluvia (%)"
    })

    st.metric(
        "📦 Registros almacenados",
        len(df)
    )

    st.dataframe(
        tabla,
        hide_index=True,
        use_container_width=True
    )