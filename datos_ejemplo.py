"""
Datos sintéticos de prueba que simulan el JSON crudo del nodo DHT22 +
sensor de suelo + sensor de lluvia, incluyendo todos los errores típicos:
texto sucio, spike, cero sospechoso, código de error, hueco temporal y duplicado.

Este archivo es solo para pruebas.
"""

DATOS_EJEMPLO = [
    {"timestamp": "2026-06-18 14:00:00", "temp_ambiente": "24.1°C", "hum_ambiente": "60%", "hum_suelo": 45, "lluvia_pct": 0},
    {"timestamp": "2026-06-18 14:00:10", "temp_ambiente": 24.3, "hum_ambiente": 61, "hum_suelo": 45, "lluvia_pct": 0},
    {"timestamp": "2026-06-18 14:00:20", "temp_ambiente": 52.0, "hum_ambiente": 60, "hum_suelo": 45, "lluvia_pct": 0},  # spike
    {"timestamp": "2026-06-18 14:00:30", "temp_ambiente": 24.2, "hum_ambiente": 0,  "hum_suelo": 45, "lluvia_pct": 0},  # 0 sospechoso
    # hueco: faltan 14:00:40 y 14:00:50 (simula caída de red corta)
    {"timestamp": "2026-06-18 14:01:00", "temp_ambiente": -999, "hum_ambiente": 58, "hum_suelo": 44, "lluvia_pct": 80},  # código de error
    {"timestamp": "2026-06-18 14:01:10", "temp_ambiente": 23.9, "hum_ambiente": 58, "hum_suelo": 44, "lluvia_pct": 75},
    {"timestamp": "2026-06-18 14:01:10", "temp_ambiente": 23.9, "hum_ambiente": 58, "hum_suelo": 44, "lluvia_pct": 75},  # duplicado
]