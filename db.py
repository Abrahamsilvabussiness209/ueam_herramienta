import pymysql


def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3307,
            database='ueam_db',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conexion
    except pymysql.MySQLError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None