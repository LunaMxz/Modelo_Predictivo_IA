# config_entrenamiento.py

CONFIG_ENTRENAMIENTO = {

    "frecuencia_resampleo": "15min",
    "columnas_agregacion_media": ["temp_ambiente", "hum_ambiente", "hum_suelo"],

    "columnas_agregacion_max": ["lluvia_pct"],

    "lookback_pasos": 192,   
    "horizon_pasos": 48,     

    "targets": ["temp_ambiente", "hum_ambiente", "hum_suelo"],

    "split": {"train": 0.70, "val": 0.15, "test": 0.15},
    "umbrales_agronomicos": {
        "temp_critica_calor": 28.0,
        "hum_ambiente_critica_hongos": 74.0,
        "hum_suelo_critica_sequia": 78.4,
        "temp_optima_min": 22.0,
        "temp_optima_max": 28.0,
        "hum_suelo_optima_min":73.3,
    },
    "pasos_lluvia_reciente": 4,
    "pasos_sostenidos_hongos": 8,
    "umbral_lluvia_significativa": 5.0,
    "porcentaje_horizonte_optimo": 0.65,

    "temp_templada_min": 18.0,
    "temp_templada_max": 30.0,
}