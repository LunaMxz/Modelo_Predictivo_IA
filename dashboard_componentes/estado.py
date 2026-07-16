import streamlit as st

from utils.estado_conexion import evaluar_conexion


def mostrar_estado(df):

    st.subheader("🟢 Estado General")

    ultima = df["timestamp"].iloc[-1]

    conexion = evaluar_conexion(ultima)

    col1, col2 = st.columns(2)

    with col1:

        if conexion["nivel"] == "en_vivo":
            st.success(f"{conexion['icono']} Sistema en vivo")
        elif conexion["nivel"] == "retrasado":
            st.warning(f"{conexion['icono']} {conexion['mensaje']}")
        else:
            st.error(f"{conexion['icono']} {conexion['mensaje']} — revisa el sensor")

    with col2:

        st.info(f"Última actualización\n\n{ultima}")

    st.divider()