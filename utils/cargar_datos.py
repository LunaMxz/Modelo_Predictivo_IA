import pandas as pd

print("SE CARGO cargar_datos.py")

def cargar_datos():

    try:

        df = pd.read_csv("data/procesado/datos_limpios.csv")

        return df

    except Exception:

        return pd.DataFrame()