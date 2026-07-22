import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # carga las variables de .env (credenciales de correo, etc.)

# from streamlit_option_menu import option_menu

from styles.estilos import cargar_estilos
from utils.datos import cargar_datos
from utils.reglas_cultivo import evaluar_estado
from utils.notificaciones import revisar_y_notificar

from auth.login import mostrar_login
from auth.registro import mostrar_registro

from vistas.inicio import mostrar_inicio
from vistas.analisis import mostrar_analisis
from vistas.dashboard_analitico import mostrar_dashboard_analitico
# from vistas.alertas import mostrar_alertas
from vistas.configuracion import mostrar_configuracion

# =====================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================

st.set_page_config(
    page_title="Agroindustria",
    page_icon="🌱",
    layout="wide"
)

cargar_estilos()
# =====================================
# VARIABLES DE SESIÓN
# =====================================

if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "login"

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "vista" not in st.session_state:
    st.session_state.vista = "Inicio"
# =====================================
# ESTILOS
# =====================================

st.markdown("""
<style>

/* Oculta Deploy */
[data-testid="stHeaderActionElements"]{
    display:none;
}

/* Oculta menú Streamlit */
#MainMenu{
    visibility:hidden;
}

/* Oculta footer */
footer{
    visibility:hidden;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background-color:#1E1F23;
}

/* Separadores */
hr{
    margin-top:8px;
    margin-bottom:8px;
}

/* Radio */

div[role="radiogroup"] label{
    padding:10px;
    border-radius:10px;
    margin-bottom:6px;
    transition:.2s;
}

div[role="radiogroup"] label:hover{
    background:#2C3138;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOGIN / REGISTRO
# =====================================

if not st.session_state.logueado:

    st.markdown("""<style>
section[data-testid="stSidebar"]{
    display:none;
}
</style>""", unsafe_allow_html=True)

    if st.session_state.pagina == "login":

        mostrar_login()

    elif st.session_state.pagina == "registro":

        mostrar_registro()

    st.stop()

# =====================================
# YA INICIÓ SESIÓN
# =====================================

st.markdown("""
<style>
section[data-testid="stSidebar"]{
    display:block;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# CARGAR DATOS
# =====================================

df = cargar_datos()

if df is None or df.empty:

    st.warning("No existe datos para mostrar.")

    st.stop()

# =====================================
# NOTIFICACIONES POR CORREO
# =====================================
# Revisa si el estado actual del cultivo empeoró respecto al último aviso
# enviado, y manda un correo si corresponde (no se repite si sigue igual).
# Se ejecuta en cada carga de la app -- recuerda que esto NO vigila 24/7
# de forma independiente, solo cuando alguien tiene la app abierta.

estado_actual = evaluar_estado(
    float(df["temp_ambiente"].iloc[-1]),
    float(df["hum_suelo"].iloc[-1]),
    float(df["hum_ambiente"].iloc[-1]) if "hum_ambiente" in df else None,
    float(df["lluvia_pct"].iloc[-1]) if "lluvia_pct" in df else None,
)

resultado_notificacion = revisar_y_notificar(estado_actual)

if resultado_notificacion is not None:

    exito, detalle = resultado_notificacion

    if exito:
        st.toast(f"📧 Alerta enviada por correo: {estado_actual['titulo']}")
    else:
        st.toast(f"⚠ No se pudo enviar la alerta por correo: {detalle}")

# =====================================
# MENÚ LATERAL
# =====================================

usuario = st.session_state["usuario"]

st.sidebar.markdown("""
<h2 style="
margin-top:-4.5px;
margin-bottom:-4px;
">
🌱 Agroindustria
</h2>
""", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.write("")

with st.sidebar:

    st.markdown("### Navegación")

    if st.button(
        "🏠   Inicio",
        use_container_width=True
    ):

        st.session_state.vista="Inicio"

        st.rerun()

    if st.button(
        "📊   Análisis",
        use_container_width=True
    ):

        st.session_state.vista="Análisis"

        st.rerun()

    if usuario.get("rol") in ("Dueño", "Agrónomo"):

        if st.button(
            "📈   Dashboard",
            use_container_width=True
        ):

            st.session_state.vista = "Dashboard"

            st.rerun()



# =====================================
# PÁGINAS
# =====================================

if st.session_state.vista == "Inicio":

    

    mostrar_inicio(df)

    

elif st.session_state.vista == "Análisis":

    mostrar_analisis(df)

elif st.session_state.vista == "Dashboard":

    mostrar_dashboard_analitico(df)

elif st.session_state.vista == "Configuración":

    mostrar_configuracion()