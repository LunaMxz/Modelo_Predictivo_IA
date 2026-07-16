import streamlit as st
import pandas as pd


def mostrar_alertas(df):

    st.subheader("🚨 Centro de Alertas")

    alertas = []

    for _, fila in df.iterrows():

        if fila["temp_ambiente"] > 30:

            alertas.append({

                "Fecha": fila["timestamp"],

                "Tipo": "🌡 Temperatura Alta",

                "Valor": f'{fila["temp_ambiente"]:.1f} °C',

                "Nivel": "Alta"

            })

        if fila["hum_suelo"] < 35:

            alertas.append({

                "Fecha": fila["timestamp"],

                "Tipo": "🌱 Humedad Baja",

                "Valor": f'{fila["hum_suelo"]:.1f} %',

                "Nivel": "Media"

            })

        if fila["lluvia_pct"] > 80:

            alertas.append({

                "Fecha": fila["timestamp"],

                "Tipo": "🌧 Lluvia Elevada",

                "Valor": f'{fila["lluvia_pct"]:.1f} %',

                "Nivel": "Baja"

            })

    if len(alertas) == 0:

        st.success("✅ No existen alertas registradas.")

    else:

        tabla = pd.DataFrame(alertas)

        st.dataframe(

            tabla,

            hide_index=True,

            use_container_width=True

        )

    st.divider()