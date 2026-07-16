import pandas as pd

from utils.conexion import obtener_conexion


def cargar_datos():

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM mediciones
        ORDER BY fecha ASC
    """)

    registros = cursor.fetchall()

    conexion.close()

    # Crear DataFrame desde los registros
    df = pd.DataFrame(registros)

    print("============== DATOS MYSQL ==============")
    print(df.head())
    print(df.dtypes)

    # Renombrar columnas
    df = df.rename(columns={
        "temperatura": "temp_ambiente",
        "humedad_ambiente": "hum_ambiente",
        "humedad_suelo": "hum_suelo",
        "lluvia": "lluvia_pct",
        "fecha": "timestamp"
    })

    # Convertir tipos
    df["temp_ambiente"] = pd.to_numeric(df["temp_ambiente"])
    df["hum_ambiente"] = pd.to_numeric(df["hum_ambiente"])
    df["hum_suelo"] = pd.to_numeric(df["hum_suelo"])
    df["lluvia_pct"] = pd.to_numeric(df["lluvia_pct"])

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df