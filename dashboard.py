import streamlit as st
import pandas as pd

from dashboard.encabezado import mostrar_encabezado
from dashboard.estado import mostrar_estado
from dashboard.kpis import mostrar_kpis
from dashboard.graficas import mostrar_graficas
from dashboard.inteligencia import mostrar_inteligencia
from dashboard.alertas import mostrar_alertas
from dashboard.estadisticas import mostrar_estadisticas
from dashboard.filtros import mostrar_filtros

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Dashboard Inteligente",
    page_icon="🌱",
    layout="wide"
)

# =====================================
# CARGAR DATOS
# =====================================

df = pd.read_csv(
    "data/procesado/datos_limpios.csv"
    
)

df = mostrar_filtros(df)

# =====================================
# DASHBOARD
# =====================================

mostrar_encabezado(df)


mostrar_estado(df)

mostrar_kpis(df)

mostrar_graficas(df)

mostrar_inteligencia(df)

mostrar_alertas(df)

mostrar_estadisticas(df)