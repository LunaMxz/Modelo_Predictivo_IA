import pymysql


def obtener_conexion():

    conexion = pymysql.connect(

        host="26.19.176.111",

        user="root2",

        password="87654321",

        database="agroindustrial",

        cursorclass=pymysql.cursors.DictCursor

    )

    return conexion