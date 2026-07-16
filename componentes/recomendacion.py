import streamlit as st


def mostrar_recomendacion(df):

    temperatura = float(df["temp_ambiente"].iloc[-1])
    humedad = float(df["hum_suelo"].iloc[-1])

    st.subheader("🤖 Recomendación Inteligente")

    if 22 <= temperatura <= 28 and humedad >= 40:

        st.success("""
### ✅ Excelente

Tu cultivo presenta condiciones óptimas.

Continúa monitoreando los sensores y mantén el sistema de riego funcionando normalmente.
""")

    elif temperatura > 30:

        st.warning("""
### 🌡 Temperatura elevada

La temperatura del invernadero es superior a la recomendada.

Se recomienda:

• Abrir ventilación.
• Activar extractores.
• Revisar la humedad del suelo.
""")

    elif humedad < 35:

        st.warning("""
### 💧 Humedad baja

El suelo presenta poca humedad.

Se recomienda realizar un riego moderado para evitar estrés en el cultivo.
""")

    else:

        st.info("""
### 🌱 Monitoreo continuo

El cultivo presenta pequeñas variaciones.

Continúa observando las condiciones durante las próximas horas.
""")

    st.divider()