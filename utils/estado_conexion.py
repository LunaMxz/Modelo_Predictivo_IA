# utils/estado_conexion.py


import pandas as pd

# A partir de cuántos minutos sin datos consideramos que algo anda mal.
# Ajusta estos valores según la frecuencia real de tus sensores.
MINUTOS_RETRASO = 2       # de 0 a 2 min: en vivo
MINUTOS_DESCONEXION = 15  # más de 15 min: probable sensor caído


def evaluar_conexion(ultimo_timestamp, ahora=None):
   
    if ahora is None:
        ahora = pd.Timestamp.now()

    ultimo_timestamp = pd.Timestamp(ultimo_timestamp)
    minutos = (ahora - ultimo_timestamp).total_seconds() / 60
    minutos = max(minutos, 0)  # por si el reloj del sensor está adelantado

    if minutos <= MINUTOS_RETRASO:
        return {
            "nivel": "en_vivo",
            "color": "#2ECC71",
            "icono": "🟢",
            "mensaje": "En vivo",
            "minutos": minutos,
        }

    if minutos <= MINUTOS_DESCONEXION:
        return {
            "nivel": "retrasado",
            "color": "#F39C12",
            "icono": "🟡",
            "mensaje": f"Última lectura hace {int(minutos)} min",
            "minutos": minutos,
        }

    horas = minutos / 60
    texto = f"Sin datos hace {int(minutos)} min" if horas < 1 else f"Sin datos hace {horas:.1f} h"

    return {
        "nivel": "desconectado",
        "color": "#E74C3C",
        "icono": "🔴",
        "mensaje": texto,
        "minutos": minutos,
    }