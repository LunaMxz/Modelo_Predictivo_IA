import streamlit as st
import plotly.express as px

from dashboard.selector import seleccionar_sensor


def mostrar_graficas(df):

    sensor, nombre = seleccionar_sensor(df)

    st.markdown("---")

    st.subheader(f"📈 {nombre}")

    fig = px.line(

        df,

        x="timestamp",

        y=sensor,

        markers=True,

        template="plotly_white"

    )

    fig.update_layout(

        height=500,

        hovermode="x unified",

        xaxis_title="Fecha",

        yaxis_title=nombre

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )