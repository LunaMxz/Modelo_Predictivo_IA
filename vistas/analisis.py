import streamlit as st
from componentes.header import mostrar_header


def mostrar_analisis(df):

    mostrar_header()

    st.title("📈 Análisis")

    st.write(
        "Aquí podrás consultar el historial completo de los datos recopilados por los sensores."
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )