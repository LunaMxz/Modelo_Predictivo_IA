import pymysql


def obtener_conexion():

    conexion = pymysql.connect(

        host="localhost",

        user="root",

        password="",

        database="mediciones_3meses",

        cursorclass=pymysql.cursors.DictCursor

    )

    return conexion