import streamlit as st

from componentes.header import mostrar_header

from dashboard_componentes.estado import mostrar_estado
from dashboard_componentes.kpis import mostrar_kpis
from dashboard_componentes.filtros import mostrar_filtros
from dashboard_componentes.graficas import mostrar_graficas
from dashboard_componentes.inteligencia import mostrar_inteligencia
from dashboard_componentes.alertas import mostrar_alertas
from dashboard_componentes.estadisticas import mostrar_estadisticas

# Roles que pueden ver esta vista más técnica/analítica. El Trabajador de
# campo se queda con el Inicio simple y accionable.
ROLES_CON_ACCESO = ["Dueño", "Agrónomo"]


def mostrar_dashboard_analitico(df):

    usuario = st.session_state.get("usuario")

    mostrar_header(df)

    # Verificación de permiso aquí también (no solo ocultando el botón
    # de navegación), igual que hicimos en Configuración.
    if usuario is None or usuario.get("rol") not in ROLES_CON_ACCESO:

        st.error(
            "No tienes permisos para ver esta sección. "
            "Disponible solo para Dueño y Agrónomo."
        )

        return

    st.title("🌱 Dashboard Analítico")

    st.caption(
        "Sistema Predictivo para la Detección Temprana de Estrés Hídrico y Térmico"
    )

    st.divider()

    # mostrar_filtros dibuja los controles de fecha en la barra lateral
    # y devuelve el DataFrame ya recortado a ese rango.
    df_filtrado = mostrar_filtros(df)

    if df_filtrado.empty:

        st.warning("No hay datos en el rango de fechas seleccionado.")

        return

    mostrar_estado(df_filtrado)

    mostrar_kpis(df_filtrado)

    mostrar_graficas(df_filtrado)

    mostrar_inteligencia(df_filtrado)

    mostrar_alertas(df_filtrado)

    mostrar_estadisticas(df_filtrado)