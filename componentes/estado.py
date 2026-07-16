import streamlit as st

from utils.reglas_cultivo import evaluar_estado


def mostrar_estado(df):

    temperatura = float(df["temp_ambiente"].iloc[-1])
    humedad_suelo = float(df["hum_suelo"].iloc[-1])
    humedad_ambiente = float(df["hum_ambiente"].iloc[-1]) if "hum_ambiente" in df else None
    lluvia = float(df["lluvia_pct"].iloc[-1]) if "lluvia_pct" in df else None

    estado = evaluar_estado(
        temperatura,
        humedad_suelo,
        humedad_ambiente,
        lluvia,
    )

    st.markdown("## Estado del cultivo")

    html_estado = f"""<div style="background:#1E1F23; border-left:6px solid {estado['color']}; border-radius:18px; padding:25px; margin-top:10px; margin-bottom:20px;">
<h3>{estado['icono']} {estado['titulo']}</h3>
<p style="color:#CFCFCF; font-size:17px; line-height:1.7;">{estado['mensaje']}</p>
<p style="color:{estado['color']}; font-size:16px; font-weight:600; margin-top:12px;">👉 {estado['accion']}</p>
</div>"""

    st.markdown(html_estado, unsafe_allow_html=True)