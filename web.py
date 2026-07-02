import streamlit as st
import pandas as pd
import pymysql

# ==========================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================

st.set_page_config(
    page_title="Greenhouse",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
div[data-testid="stMetric"]{
    background-color:#111827;
    border:1px solid #2d3748;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 4px 10px rgba(0,0,0,.3);
}

div[data-testid="stMetric"]:hover{
    border:1px solid #00c853;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# ENCABEZADO
# ==========================

st.title("Agroindustria")

st.subheader("Sistema Inteligente de Monitoreo para Invernaderos")

st.markdown("---")

st.write("""
Este sistema permite visualizar el estado del cultivo mediante sensores IoT.

Actualmente los datos se leen desde un archivo CSV de prueba.
Más adelante la información se obtendrá automáticamente desde la base de datos.
""")

# ==========================
# MENÚ
# ==========================

st.sidebar.title("Menú")

st.sidebar.radio(
    "Selecciona una opción",
    [
        "Inicio",
        "Dashboard",
        "Análisis",
        "Base de datos",
        "Configuración"
    ]
)

# ==========================
# CONEXIÓN A LA BASE DE DATOS
# ==========================

def conectar_db():

    conexion = pymysql.connect(
        host="10.0.13.217",      
        user="modelo",           
        password="12345678",           
        database="agroindustrial",       
        port=3306
    )

    return conexion


# ==========================
# CARGAR DATOS
# ==========================

def cargar_datos():

    

    #df = pd.read_csv("data/procesado/datos_limpios.csv")

    #return df

    
    conexion = conectar_db()
    
    consulta = """
SELECT *
FROM mediciones
ORDER BY fecha DESC
"""
    
    df = pd.read_sql(consulta, conexion)

    conexion.close()

    return df


# 
# LEER DATOS
#

df = cargar_datos()

# Copia para métricas
df_metricas = df.copy()

# Cambiar nombres para mostrar
df = df.rename(columns={
    "id": "ID",
    "temperatura": "Temperatura (°C)",
    "humedad_ambiente": "Humedad ambiente (%)",
    "humedad_suelo": "Humedad del suelo (%)",
    "lluvia": "Lluvia (%)",
    "fecha": "Fecha y hora"
})

# ==========================
# INDICADORES
# ==========================

st.header("Estado actual del cultivo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌡 Temperatura",
        f"{df_metricas['temperatura'].iloc[-1]:.1f} °C"
    )

with col2:
    st.metric(
        "💧 Humedad ambiente",
        f"{df_metricas['humedad_ambiente'].iloc[-1]:.1f} %"
    )

with col3:
    st.metric(
        "🌱 Humedad del suelo",
        f"{df_metricas['humedad_suelo'].iloc[-1]:.1f} %"
    )

with col4:
    st.metric(
        "🌧 Lluvia",
        f"{df_metricas['lluvia'].iloc[-1]:.1f} %"
    )

st.markdown("---")

# ==========================
# ESTADO DEL CULTIVO
# ==========================

temp = df_metricas["temperatura"].iloc[-1]
hum = df_metricas["humedad_suelo"].iloc[-1]

if 22 <= temp <= 28 and hum >= 40:
    st.success("🟢 Estado del cultivo: ÓPTIMO")

elif temp > 30:
    st.warning("🟡 Temperatura elevada")

else:
    st.error("🔴 Revisar condiciones del cultivo")

# ==========================
# INFORMACIÓN GENERAL
# ==========================

st.metric(
    "Registros almacenados",
    len(df)
)

# ==========================
# HISTORIAL
# ==========================

st.header("Historial de datos")

st.dataframe(
    df.tail(20),
    hide_index=True,
    use_container_width=True
)