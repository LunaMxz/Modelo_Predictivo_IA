import streamlit as st

def mostrar_alertas(df):

    st.title("🔔 Alertas")

    temperatura = df["temp_ambiente"].iloc[-1]
    humedad = df["hum_suelo"].iloc[-1]
    lluvia = df["lluvia_pct"].iloc[-1]

    if temperatura > 30:
        st.warning("🌡 Temperatura elevada. Revise el sistema de ventilación.")

    elif humedad < 30:
        st.error("🌱 Humedad del suelo baja. Se recomienda regar el cultivo.")

    elif lluvia > 80:
        st.info("🌧 Se detectó una alta probabilidad de lluvia.")

    else:
        st.success("✅ No existen alertas por el momento.")