# config.py

CONFIG = {
    "frecuencia_esperada": "10s",
    "rangos_validos": {
        "temp_ambiente": (-10, 60),
        "hum_ambiente": (0, 100),
        "hum_suelo": (0, 100),
        "lluvia_pct": (0, 100),
    },
    "error_values": [-999, 999, -1, 9999, -9999],
    "columnas_cero": ["hum_ambiente", "hum_suelo"],
    "max_delta_por_lectura": {
        "temp_ambiente": 1.5,   
        "hum_ambiente": 5,      
        "hum_suelo": 2,         
    },
    "ventana_promedio_relleno": 30, 
    "limite_relleno": 30,  
    "limite_relleno_lluvia": 2,
    "columnas_numericas": ["temp_ambiente", "hum_ambiente", "hum_suelo", "lluvia_pct"],

    "ruta_salida_csv": "data/procesado/datos_limpios.csv",

}
