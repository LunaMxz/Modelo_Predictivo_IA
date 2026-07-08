import streamlit as st


def mostrar_estadisticas(df):

    st.subheader("📊 Estadísticas del Cultivo")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🌡 Temperatura máxima",
            f"{df['temp_ambiente'].max():.1f} °C"
        )

        st.metric(
            "🌡 Temperatura mínima",
            f"{df['temp_ambiente'].min():.1f} °C"
        )

    with col2:

        st.metric(
            "💧 Humedad ambiente promedio",
            f"{df['hum_ambiente'].mean():.1f} %"
        )

        st.metric(
            "🌱 Humedad suelo mínima",
            f"{df['hum_suelo'].min():.1f} %"
        )

    with col3:

        st.metric(
            "🌧 Lluvia máxima",
            f"{df['lluvia_pct'].max():.1f} %"
        )

        st.metric(
            "📦 Registros",
            len(df)
        )

    st.divider()

    st.subheader("📋 Resumen")

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"""
### Información del monitoreo

🕒 Último registro

{df['timestamp'].iloc[-1]}

📅 Primer registro

{df['timestamp'].iloc[0]}

📦 Total de registros

{len(df)}
""")

    with col2:

        st.info(f"""
### Promedios

🌡 Temperatura: **{df['temp_ambiente'].mean():.1f} °C**

💧 Humedad ambiente: **{df['hum_ambiente'].mean():.1f}%**

🌱 Humedad suelo: **{df['hum_suelo'].mean():.1f}%**

🌧 Lluvia: **{df['lluvia_pct'].mean():.1f}%**
""")

    st.divider()