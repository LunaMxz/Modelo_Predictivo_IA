import streamlit as st

def mostrar_analisis(df):

    st.title("📈 Análisis")

    st.write(
        "Aquí podrás consultar el historial completo de los datos recopilados por los sensores."
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )