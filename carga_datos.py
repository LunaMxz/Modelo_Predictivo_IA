#carga_datos.py 

"""
carga segura de datos cudos, Tolera:

  - JSON con sintaxis rota en registros individuales (los descarta, no tumba el proceso completo)
  - NDJSON (un objeto JSON por línea), común en streams de sensores
  - Estructura anidada variable: {"sensores": {...}}        
"""

import json
import pandas as pd


def cargar_json_seguro(ruta_o_lista):

    registros_validos = []
    registros_descartados = []

    if isinstance(ruta_o_lista, str):
        with open(ruta_o_lista, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
        try:
            data = json.loads(contenido)
            crudos = data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            crudos = []
            for i, linea in enumerate(contenido.splitlines()): #NDJSON lee linea por linea 
                linea = linea.strip().rstrip(",")
                if not linea:
                    continue
                try:
                    crudos.append(json.loads(linea))
                except json.JSONDecodeError as e:
                    registros_descartados.append({"linea": i, "contenido": linea, "error": str(e)})
    else:
        crudos = ruta_o_lista  # ya es una lista de dicts en memoria

    for registro in crudos:
        if not isinstance(registro, dict):
            registros_descartados.append({"contenido": registro, "error": "no es un objeto JSON"})
            continue
        # Estructura anidada variable
        if "sensores" in registro and isinstance(registro["sensores"], dict):
            plano = {**{k: v for k, v in registro.items() if k != "sensores"}, **registro["sensores"]}
        else:
            plano = registro
        registros_validos.append(plano)

    if registros_descartados:
        print(f"[AVISO] {len(registros_descartados)} registros con sintaxis JSON inválida fueron descartados.")

    return pd.DataFrame(registros_validos)