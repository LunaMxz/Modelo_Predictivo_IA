# carga_mysql.py
import pandas as pd
from sqlalchemy import create_engine, text

try:
    # Caso 1: se importa conexionDB
    from .credenciales import DB_CONFIG
except ImportError:
    # Caso 2: se corre directamente dentro de esta carpeta
    from credenciales import DB_CONFIG

RENOMBRE_COLUMNAS = {
    "fecha": "timestamp",
    "temperatura": "temp_ambiente",
    "humedad_ambiente": "hum_ambiente",
    "humedad_suelo": "hum_suelo",
    "lluvia": "lluvia_pct",
}


def cargar_desde_mysql():
    url_conexion = (
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(url_conexion)

    query = text("SELECT * FROM mediciones ORDER BY fecha ASC")
    df = pd.read_sql(query, con=engine)

    df = df.rename(columns=RENOMBRE_COLUMNAS)
    df = df.drop(columns=["id"], errors="ignore")
    return df


if __name__ == "__main__":
    print("[Python] Conectando a MariaDB...")
    df = cargar_desde_mysql()
    print(f"[Python] ¡Éxito! Registros leídos de MariaDB: {len(df)}")
    print("\nPrimeras filas del dataset:")
    print(df.head())