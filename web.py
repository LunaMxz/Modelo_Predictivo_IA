import streamlit as st

from utils.leer_csv import cargar_datos
from auth.login import mostrar_login
from vistas.inicio import mostrar_inicio
from vistas.analisis import mostrar_analisis
from vistas.alertas import mostrar_alertas
from vistas.configuracion import mostrar_configuracion
from auth.registro import mostrar_registro



#sesion del usuario


if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "login"    



# =====================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================

st.set_page_config(
    page_title="Agroindustria",
    page_icon="🌱",
    layout="wide"
)

# =====================================
# ESTILOS
# =====================================

st.markdown("""
<style>

/* Oculta el botón Deploy */
[data-testid="stHeaderActionElements"]{
    display:none;
}

/* Oculta el menú de los tres puntos */
#MainMenu{
    visibility:hidden;
}

/* Oculta el footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

#cargar datos


df = cargar_datos()

# =====================================
# LOGIN
# =====================================

if not st.session_state.logueado:

    st.markdown("""
        <style>
        section[data-testid="stSidebar"]{
        display:none;
        }
        </style>
        """, unsafe_allow_html=True)
 
    if st.session_state.pagina == "login":

        mostrar_login()

    elif st.session_state.pagina == "registro":
        mostrar_registro()

    st.stop()

# =====================================
# MENÚ LATERAL
# =====================================

st.sidebar.title("🌱 Agroindustria")

opcion = st.sidebar.radio(

    "Navegación",

    [
        "🏠 Inicio",
        "📈 Análisis",
        "🔔 Alertas",
        "⚙ Configuración"
    ]

)






# =====================================
# PÁGINA INICIO
# =====================================

if opcion == "🏠 Inicio":

    mostrar_inicio(df)

# =====================================
# PÁGINA ANÁLISIS
# =====================================

elif opcion == "📈 Análisis":

    mostrar_analisis(df)

# =====================================
# PÁGINA ALERTAS
# =====================================

elif opcion == "🔔 Alertas":

    mostrar_alertas(df)

# =====================================
# CONFIGURACIÓN
# =====================================

elif opcion == "⚙ Configuración":

    mostrar_configuracion()