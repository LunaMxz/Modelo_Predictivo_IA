import streamlit as st
from datetime import datetime

from utils.reglas_cultivo import evaluar_estado
from utils.estado_conexion import evaluar_conexion


def mostrar_header(df=None):

    usuario = st.session_state.get("usuario")

    if usuario is None:
        return

    nombre = usuario["nombre"]
    correo = usuario["correo"]
    rol = usuario.get("rol", "Usuario")

    # =====================================
    # SALUDO
    # =====================================

    hora = datetime.now().hour

    if hora < 12:
        saludo = "☀ Buenos días"
    elif hora < 19:
        saludo = "🌤 Buenas tardes"
    else:
        saludo = "🌙 Buenas noches"

    fecha = datetime.now().strftime("%d/%m/%Y")

    # =====================================
    # ESTADO DE CONEXIÓN (calculado una sola vez, se usa abajo)
    # =====================================

    conexion = None

    if df is not None and "timestamp" in df and len(df) > 0:
        conexion = evaluar_conexion(df["timestamp"].iloc[-1])

    # =====================================
    # HEADER
    # =====================================

    col1, col_sync, col2, col3 = st.columns([6, 2, 1, 1])

    with col1:

        logo, texto = st.columns([1, 7])

        with logo:

            st.image(
                "imagenes/logo.jpeg",
                width=65
            )

        with texto:

            html = f"""<div style="padding-top:5px;">
<h2 style="color:#57C84D; margin-bottom:0px;">Agroindustria</h2>
<p style="color:#B5B5B5; margin-top:0px; font-size:15px;">{saludo}, <b>{nombre}</b></p>
<p style="color:#8D8D8D; font-size:13px; margin-top:-10px;">📅 {fecha}</p>
</div>"""

            st.markdown(html, unsafe_allow_html=True)

    # =====================================
    # BADGE DE SINCRONIZACIÓN (siempre visible, no escondido en un popover)
    # =====================================

    with col_sync:

        if conexion is not None:

            st.markdown(f"""<div style="padding-top:28px; text-align:center;">
<span style="background:{conexion['color']}22; color:{conexion['color']}; padding:6px 14px;
border-radius:20px; font-size:14px; font-weight:600; border:1px solid {conexion['color']}55;
white-space:nowrap;">
{conexion['icono']} {conexion['mensaje']}
</span>
</div>""", unsafe_allow_html=True)

    # =====================================
    # NOTIFICACIONES
    # =====================================

    with col2:

        with st.popover("🔔"):

            st.subheader("Notificaciones")

            st.divider()

            if df is not None and len(df) > 0:

                estado_cultivo = evaluar_estado(
                    float(df["temp_ambiente"].iloc[-1]),
                    float(df["hum_suelo"].iloc[-1]),
                    float(df["hum_ambiente"].iloc[-1]) if "hum_ambiente" in df else None,
                    float(df["lluvia_pct"].iloc[-1]) if "lluvia_pct" in df else None,
                )

                if estado_cultivo["nivel"] == "critico":
                    st.error(f"{estado_cultivo['icono']} {estado_cultivo['titulo']}")
                elif estado_cultivo["nivel"] == "atencion":
                    st.warning(f"{estado_cultivo['icono']} {estado_cultivo['titulo']}")
                else:
                    st.success(f"{estado_cultivo['icono']} {estado_cultivo['titulo']}")

                if conexion is not None:
                    st.info(f"{conexion['icono']} {conexion['mensaje']}")
                    st.caption(f"Última lectura registrada: {df['timestamp'].iloc[-1]}")

            else:

                st.info("Aún no hay datos de los sensores.")

    # =====================================
    # PERFIL
    # =====================================

    with col3:

        with st.popover("👤"):

            html_perfil = f"""<div style="text-align:center;">
<div style="font-size:55px;">👨🏻‍🌾</div>
<h3 style="margin-bottom:0px;">{nombre}</h3>
<p style="color:#AFAFAF;">{correo}</p>
<p>👤 {rol}</p>
<p style="color:#57C84D;">🟢 En línea</p>
</div>"""

            st.markdown(html_perfil, unsafe_allow_html=True)

            st.divider()

            if rol == "Dueño":

                if st.button(
                    "⚙ Configuración",
                    use_container_width=True
                ):

                    st.session_state.vista = "Configuración"
                    st.rerun()

            if st.button(
                "🚪 Cerrar sesión",
                type="primary",
                use_container_width=True
            ):

                st.session_state.logueado = False
                st.session_state.usuario = None
                st.session_state.pagina = "login"
                st.rerun()

    st.divider()