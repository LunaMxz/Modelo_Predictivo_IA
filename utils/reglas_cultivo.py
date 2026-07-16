# utils/reglas_cultivo.py


UMBRALES = {
    "temp_ideal_min": 22,
    "temp_ideal_max": 28,
    "temp_alta": 30,
    "hum_suelo_ideal": 40,
    "hum_suelo_baja": 35,
    "lluvia_alta": 80,
}


def evaluar_estado(temperatura, humedad_suelo, humedad_ambiente=None, lluvia=None):
    
    u = UMBRALES

    temp_ok = u["temp_ideal_min"] <= temperatura <= u["temp_ideal_max"]
    humedad_ok = humedad_suelo >= u["hum_suelo_ideal"]

    # --- Crítico: temperatura alta y suelo seco al mismo tiempo ---
    if temperatura > u["temp_alta"] and humedad_suelo < u["hum_suelo_baja"]:
        return {
            "nivel": "critico",
            "color": "#E74C3C",
            "icono": "🔴",
            "titulo": "Riesgo de estrés hídrico",
            "mensaje": "La planta está perdiendo agua más rápido de lo que el suelo puede darle.",
            "accion": "Riega ahora y revisa la ventilación en los próximos 30 minutos.",
            "riesgo_pct": 90,
        }

    # --- Temperatura alta sola ---
    if temperatura > u["temp_alta"]:
        return {
            "nivel": "atencion",
            "color": "#F39C12",
            "icono": "🟡",
            "titulo": "Temperatura elevada",
            "mensaje": "El invernadero está más caliente de lo recomendado.",
            "accion": "Abre la ventilación o activa los extractores en la próxima hora.",
            "riesgo_pct": 60,
        }

    # --- Suelo seco solo ---
    if humedad_suelo < u["hum_suelo_baja"]:
        return {
            "nivel": "atencion",
            "color": "#F39C12",
            "icono": "🟡",
            "titulo": "Humedad del suelo baja",
            "mensaje": "El suelo tiene menos agua de la que el cultivo necesita.",
            "accion": "Riega en las próximas 2 horas.",
            "riesgo_pct": 60,
        }

    # --- Lluvia alta (informativo, no urgente) ---
    if lluvia is not None and lluvia > u["lluvia_alta"]:
        return {
            "nivel": "atencion",
            "color": "#3498DB",
            "icono": "🌧",
            "titulo": "Alta probabilidad de lluvia",
            "mensaje": "Se detectó lluvia intensa en la zona.",
            "accion": "Revisa que el drenaje del invernadero esté despejado.",
            "riesgo_pct": 35,
        }

    # --- Todo bien ---
    if temp_ok and humedad_ok:
        return {
            "nivel": "ok",
            "color": "#2ECC71",
            "icono": "🟢",
            "titulo": "Cultivo saludable",
            "mensaje": "Las condiciones actuales son ideales para el cultivo.",
            "accion": "No se requiere ninguna acción por ahora.",
            "riesgo_pct": 15,
        }

    # --- Caso intermedio: sin alerta puntual, pero fuera del rango ideal ---
    return {
        "nivel": "atencion",
        "color": "#F39C12",
        "icono": "🟡",
        "titulo": "Fuera del rango ideal",
        "mensaje": "Las condiciones se alejan un poco de lo recomendado, sin ser críticas todavía.",
        "accion": "Supervisa el cultivo durante las próximas horas.",
        "riesgo_pct": 40,
    }


# Nombres amigables para mostrar columnas técnicas en cualquier tabla o gráfica
NOMBRES_AMIGABLES = {
    "temp_ambiente": "Temperatura",
    "hum_ambiente": "Humedad ambiente",
    "hum_suelo": "Humedad del suelo",
    "lluvia_pct": "Lluvia",
    "timestamp": "Fecha y hora",
}