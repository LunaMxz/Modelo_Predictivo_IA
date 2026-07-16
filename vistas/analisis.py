import streamlit as st
from componentes.header import mostrar_header
from utils.reglas_cultivo import NOMBRES_AMIGABLES


def mostrar_analisis(df):

    mostrar_header(df)

    st.title("📈 Análisis")

    st.write(
        "Aquí podrás consultar el historial completo de los datos recopilados por los sensores."
    )

    # Mostramos nombres legibles sin modificar el DataFrame original
    df_visible = df.rename(columns=NOMBRES_AMIGABLES)

    st.dataframe(
        df_visible,
        use_container_width=True,
        hide_index=True
    )