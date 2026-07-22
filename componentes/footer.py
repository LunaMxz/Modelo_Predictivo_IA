import streamlit as st

from utils.estado_conexion import evaluar_conexion


def mostrar_footer(df=None):

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
### 🌱 Agroindustria

Monitoreo inteligente para cultivos en invernadero mediante sensores IoT e Inteligencia Artificial.
""")

    with col2:

        if df is not None and "timestamp" in df and len(df) > 0:

            conexion = evaluar_conexion(df["timestamp"].iloc[-1])

            ultima = df["timestamp"].iloc[-1]

            st.markdown(f"""
### 📡 Estado del sistema

{conexion['icono']} {conexion['mensaje']}

🕒 Última actualización

**{ultima}**
""")

        else:

            st.markdown("""
### 📡 Estado del sistema

🔴 Sin datos disponibles
""")

    with col3:

        st.markdown("""
### ℹ Información

Versión **1.0**

Proyecto IoT + IA

Universidad Tecnológica
""")

    st.markdown("---")

    st.markdown(
        '<div style="text-align:center;color:#9E9E9E;font-size:14px;">'
        '© 2026 <b>Agroindustria</b> · Todos los derechos reservados'
        '</div>',
        unsafe_allow_html=True
    )