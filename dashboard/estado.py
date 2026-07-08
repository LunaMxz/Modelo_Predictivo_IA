import streamlit as st


def mostrar_estado(df):

    st.subheader("🟢 Estado General")

    ultima = df["timestamp"].iloc[-1]

    col1, col2 = st.columns(2)

    with col1:

        st.success("Sistema operativo")

    with col2:

        st.info(f"Última actualización\n\n{ultima}")

    st.divider()