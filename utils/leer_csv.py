import pandas as pd

def cargar_datos():

    try:
        return pd.read_csv("data/procesado/datos_limpios.csv")
    except Exception:
        return pd.DataFrame()