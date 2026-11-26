# Arranque main.py del software UEAM (Estable y sin cierres en navegación)
import os
import eel
from db import obtener_conexion  # <-- Importamos tu conexión a MySQL
from backend.auth import autenticar_usuario
from backend.diagnostico import ejecutar_mantenimiento_logico, escanear_sistema as escanear_backend
from backend.documental import listar_documentos, registrar_documento
from backend.seguridad import generar_respaldo_sistema
from backend.pdf_generator import generar_pdf_diagnostico


@eel.expose
def login_user(username, password=""):
    return autenticar_usuario(username, password)


@eel.expose
def escanear_sistema(codigo_equipo):
    return escanear_backend(codigo_equipo)


@eel.expose
def procesar_mantenimiento(datos):
    return ejecutar_mantenimiento_logico(datos)


@eel.expose
def exportar_pdf_reporte(datos):
    return generar_pdf_diagnostico(datos)


@eel.expose
def obtener_documentos():
    return listar_documentos()


@eel.expose
def guardar_documento(nombre, categoria, usuario):
    return registrar_documento(nombre, categoria, usuario)


@eel.expose
def crear_backup():
    return generar_respaldo_sistema()


if __name__ == "__main__":
    # Verificación rápida de la conexión a MySQL antes de levantar Eel
    conexion_test = obtener_conexion()
    if conexion_test:
        print("¡Conexión a la base de datos 'ueam_dh' establecida correctamente!")
        conexion_test.close()
    else:
        print("Advertencia: No se pudo conectar a la base de datos en XAMPP. Revisa que esté encendido.")

    web_folder = os.path.join(os.path.dirname(__file__), 'web')
    eel.init(web_folder)

    # Iniciamos en login.html absoluto de manera limpia y estable
    eel.start(
        'views/login.html',
        mode='default',
        size=(1024, 728),
        port=8080
    )
