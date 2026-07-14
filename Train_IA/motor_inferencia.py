# motor_inferencia.py
import numpy as np

def _hay_racha_sostenida(condicion_booleana, pasos_requeridos):
    """
    condicion_booleana: array 1D de True/False por paso de tiempo.
    Devuelve True si existe una racha de al menos `pasos_requeridos`
    pasos CONSECUTIVOS en True.
    """
    racha_actual = 0
    for valor in condicion_booleana:
        racha_actual = racha_actual + 1 if valor else 0
        if racha_actual >= pasos_requeridos:
            return True
    return False

def generar_alertas(pred_temp, pred_hum_ambiente, pred_hum_suelo,
                     lluvia_reciente, config_entrenamiento):

    umbrales = config_entrenamiento["umbrales_agronomicos"]
    pasos_sostenidos = config_entrenamiento["pasos_sostenidos_hongos"]
    porcentaje_horizonte_optimo = config_entrenamiento["porcentaje_horizonte_optimo"]
    umbral_lluvia_significativa = config_entrenamiento["umbral_lluvia_significativa"]
    temp_templada_min = config_entrenamiento["temp_templada_min"]
    temp_templada_max = config_entrenamiento["temp_templada_max"]

    alertas = {
        "crecimiento_optimo": False,
        "estres_hidrico": False,
        "escudo_fungico": False,
    }

    temp_en_rango = (pred_temp >= umbrales["temp_optima_min"]) & \
                     (pred_temp <= umbrales["temp_optima_max"])
    suelo_en_rango = pred_hum_suelo >= umbrales["hum_suelo_optima_min"]
    ambas_en_rango = temp_en_rango & suelo_en_rango
    alertas["crecimiento_optimo"] = bool(
        np.mean(ambas_en_rango) >= porcentaje_horizonte_optimo
    )

    suelo_critico = np.any(pred_hum_suelo < umbrales["hum_suelo_critica_sequia"])
    hubo_lluvia_reciente = np.max(lluvia_reciente) > umbral_lluvia_significativa
    alertas["estres_hidrico"] = bool(suelo_critico and not hubo_lluvia_reciente)

    hum_favorable_hongos = pred_hum_ambiente > umbrales["hum_ambiente_critica_hongos"]
    temp_favorable_hongos = (pred_temp >= temp_templada_min) & \
                             (pred_temp <= temp_templada_max)
    condicion_combinada = hum_favorable_hongos & temp_favorable_hongos
    alertas["escudo_fungico"] = _hay_racha_sostenida(condicion_combinada, pasos_sostenidos)

    return alertas