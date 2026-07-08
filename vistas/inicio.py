import streamlit as st
from componentes.header import mostrar_header

def mostrar_inicio(df):

    # =====================================
    # ENCABEZADO
    # =====================================
    
    mostrar_header()

    st.markdown("""
    <h1 style='margin-bottom:0px;'>🌱 Agroindustria</h1>

    <h4 style='color:gray;margin-top:0px;'>
    Sistema Inteligente de Monitoreo para Invernaderos
    </h4>

    <p style='font-size:17px;'>

    Monitorea en tiempo real el estado de tu cultivo mediante
    sensores IoT, analítica de datos e inteligencia artificial.

    </p>
    """, unsafe_allow_html=True)

    st.divider()

    # =====================================
    # ESTADO DEL CULTIVO
    # =====================================

    st.subheader("Estado del cultivo")

    ultima_actualizacion = df["timestamp"].iloc[-1]

    st.caption(f"🕒 Última actualización: {ultima_actualizacion}")

    temperatura = df["temp_ambiente"].iloc[-1]
    humedad = df["hum_suelo"].iloc[-1]

    if 22 <= temperatura <= 28 and humedad >= 40:

        st.success("""
        ### Cultivo saludable

        Todos los parámetros se encuentran dentro de los rangos recomendados.

        El cultivo presenta condiciones óptimas para su desarrollo.
        """)

    elif temperatura > 30:

        st.warning("""
        ### ⚠ Temperatura elevada

        Se recomienda revisar el sistema de ventilación del invernadero.
        """)

    else:

        st.error("""
        ###  Atención requerida

        Se detectaron condiciones fuera de los rangos recomendados.
        """)

    st.divider()

    # =====================================
    # MÉTRICAS
    # =====================================

    st.subheader("Sensores en tiempo real")

    # Estilos de las tarjetas
    st.markdown("""
    <style>

    .card{
        background-color:#262730;
        border:1px solid #3A3B45;
        border-radius:16px;
        padding:22px;
        min-height:180px;
        box-shadow:0px 2px 8px rgba(0,0,0,.25);
    }

    .titulo-card{
        color:#BFC5D2;
        font-size:18px;
        margin-bottom:25px;
    }

    .valor-card{
        color:#58D68D;
        font-size:40px;
        font-weight:bold;
        margin-bottom:20px;
    }

    .sub-card{
        color:#8D99AE;
        font-size:14px;
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

            st.markdown(f"""
            <div class="card">

            <div class="titulo-card">
                    🌡 Temperatura
            </div>

            <div class="valor-card">
                    {temperatura:.1f} °C
            </div>

            <div class="sub-card">
                    Temperatura actual
            </div>

            </div>
            """, unsafe_allow_html=True)

    with col2:

            st.markdown(f"""
            <div class="card">

            <div class="titulo-card">
                    💧 Humedad ambiente
            </div>

            <div class="valor-card">
                    {df['hum_ambiente'].iloc[-1]:.1f} %
            </div>

            <div class="sub-card">
                    Sensor ambiental
            </div>

            </div>
            """, unsafe_allow_html=True)

    with col3:

            st.markdown(f"""
            <div class="card">

            <div class="titulo-card">
                    🌱 Humedad del suelo
            </div>

            <div class="valor-card">
                    {df['hum_ambiente'].iloc[-1]:.1f} %
            </div>

            <div class="sub-card">
                    Nivel de humedad
            </div>

            </div>
            """, unsafe_allow_html=True)

    with col4:

            st.markdown(f"""
            <div class="card">

            <div class="titulo-card">
                🌧 Lluvia
            </div>

            <div class="valor-card">
                {df['hum_ambiente'].iloc[-1]:.1f} %
            </div>

            <div class="sub-card">
                Precipitación detectada
            </div>

            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # =====================================
    # GRÁFICA
    # =====================================

    st.subheader(" Comportamiento del cultivo")

    st.line_chart(
        df.set_index("timestamp")[
            [
                "temp_ambiente",
                "hum_ambiente"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    # =====================================
    # TABLA
    # =====================================

    st.subheader(" Últimos registros")

    tabla = df.tail(10).rename(columns={

        "timestamp": "Fecha",

        "temp_ambiente": "Temperatura (°C)",

        "hum_ambiente": "Humedad ambiente (%)",

        "hum_suelo": "Humedad del suelo (%)",

        "lluvia_pct": "Lluvia (%)"

    })

    st.metric(
        " Registros almacenados",
        len(df)
    )

    st.dataframe(
        tabla,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # FOOTER
    # =====================================

    st.caption(
        "🌱 Agroindustria | Proyecto desarrollado para el monitoreo inteligente de cultivos mediante sensores IoT e Inteligencia Artificial."
    )