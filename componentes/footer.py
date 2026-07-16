import streamlit as st
from datetime import datetime


def mostrar_footer():

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
### 🌱 Agroindustria

Monitoreo inteligente para cultivos en invernadero mediante sensores IoT e Inteligencia Artificial.
""")

    with col2:

        st.markdown(f"""
### 📡 Estado del sistema

🟢 Conectado

🕒 Última actualización

**{fecha}**
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