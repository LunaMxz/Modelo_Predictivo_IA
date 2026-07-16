import streamlit as st

from utils.prediccion_ia import predecir_estado_futuro


def mostrar_pronostico_ia(df):

    st.subheader("🤖 Pronóstico con IA")

    resultado = predecir_estado_futuro(df)

    if resultado is None:

        st.info(
            "Aún no hay suficiente historial limpio (se necesitan aproximadamente "
            "48 horas) para generar el pronóstico con IA. Esta sección se activará "
            "automáticamente en cuanto haya datos suficientes."
        )

        st.divider()

        return

    horas = resultado["horas_pronosticadas"]
    alertas = resultado["alertas"]

    st.caption(f"Basado en el historial reciente, proyectando las próximas {horas:.0f} horas.")

    hubo_alerta = False

    if alertas["estres_hidrico"]:

        hubo_alerta = True

        st.error(
            "🔴 **Riesgo de estrés hídrico.** El modelo prevé humedad del suelo "
            "por debajo del nivel seguro, sin lluvia reciente que lo compense.\n\n"
            "👉 Considera regar en las próximas horas."
        )

    if alertas["escudo_fungico"]:

        hubo_alerta = True

        st.warning(
            "🟡 **Condiciones favorables para hongos.** Se prevé humedad alta y "
            "temperatura templada sostenidas por un período prolongado.\n\n"
            "👉 Vigila el follaje y considera mejorar la ventilación."
        )

    if not hubo_alerta:

        if alertas["crecimiento_optimo"]:

            st.success(
                "🟢 Se esperan condiciones óptimas para el cultivo durante la "
                "mayor parte de las próximas horas."
            )

        else:

            st.info(
                "Se esperan condiciones mixtas: sin alertas específicas, aunque "
                "fuera del rango ideal en algunos momentos."
            )

    with st.expander("Ver detalle numérico del pronóstico"):

        st.write(f"Temperatura promedio prevista: {resultado['pred_temp_promedio']:.1f} °C")

        st.write(f"Temperatura máxima prevista: {resultado['pred_temp_max']:.1f} °C")

        st.write(f"Humedad del suelo mínima prevista: {resultado['pred_hum_suelo_min']:.1f} %")

    st.divider()