# verificar_bd.py
"""
Script de diagnóstico -- NO forma parte de la app, es solo para revisar
cuántos registros hay en cada base de datos local antes de decidir a
cuál debe apuntar utils/conexion.py.

Corre esto parado en la raíz del proyecto:
    python verificar_bd.py
"""

import pymysql


def contar_filas(nombre_bd, usuario, password, tabla="mediciones"):

    try:

        conexion = pymysql.connect(
            host="localhost",
            user=usuario,
            password=password,
            database=nombre_bd,
        )

        cursor = conexion.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")

        total = cursor.fetchone()[0]

        cursor.execute(f"SELECT MIN(fecha), MAX(fecha) FROM {tabla}")

        rango = cursor.fetchone()

        conexion.close()

        return f"✅ {total} filas -- desde {rango[0]} hasta {rango[1]}"

    except Exception as e:

        return f"❌ No se pudo leer: {e}"


print("=== mediciones_3meses (la que usa tu dashboard hoy) ===")
print(contar_filas("mediciones_3meses", "root", ""))

print()

print("=== agrodata (la que usó Train_IA para entrenar) ===")
print(contar_filas("agrodata", "root", "12345678"))