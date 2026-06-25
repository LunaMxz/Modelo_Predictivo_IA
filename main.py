import sys
import os

from config import CONFIG
from carga_datos import cargar_json_seguro
from limpieza import pipeline_limpieza_invernadero
from datos_ejemplo import DATOS_EJEMPLO


def main():
    if len(sys.argv) > 1:
        fuente = sys.argv[1]
        print(f"Cargando datos reales desde: {fuente}")
    else:
        fuente = DATOS_EJEMPLO
        print("No se especificó archivo. Usando datos de ejemplo para prueba.")

    print("_" * 60)
    print("PASO 1: Carga segura de datos")
    print("_" * 60)
    df_crudo = cargar_json_seguro(fuente)
    print(f"Registros cargados: {len(df_crudo)}")

    print("\n" + "_" * 60)
    print("Pipeline de limpieza")
    print("_ " * 60)
    df_limpio = pipeline_limpieza_invernadero(df_crudo, CONFIG)
    print(f"Registros tras limpieza (incluye huecos reconstruidos): {len(df_limpio)}")

    # Guardar resultado 
    ruta_salida = CONFIG["ruta_salida_csv"]
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df_limpio.round(3).to_csv(ruta_salida)
    print(f"\nDataset limpio guardado en: {ruta_salida}")

    print("\nVista previa del resultado:\n")
    print(df_limpio.to_string())

    return df_limpio


if __name__ == "__main__":
    main()