# ⚠ ARCHIVO EN DESUSO ⚠
# Esta pantalla ya vive dentro de web.py como "vistas/dashboard_analitico.py",
# conectada a la base de datos real (no a este CSV de prueba).
# Ya no corras "streamlit run dashboard.py" -- usa "streamlit run web.py".
# Se deja este archivo por ahora solo como referencia histórica.

import streamlit as st
import pandas as pd

from dashboard_componentes.encabezado import mostrar_encabezado
from dashboard_componentes.estado import mostrar_estado
from dashboard_componentes.kpis import mostrar_kpis
from dashboard_componentes.graficas import mostrar_graficas
from dashboard_componentes.inteligencia import mostrar_inteligencia
from dashboard_componentes.alertas import mostrar_alertas
from dashboard_componentes.estadisticas import mostrar_estadisticas
from dashboard_componentes.filtros import mostrar_filtros

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