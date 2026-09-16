# Arranque main.py del software

import os
import sys
import time
import eel
from backend.auth import autenticar_usuario
from backend.diagnostico import ejecutar_mantenimiento_logico, escanear_sistema as escanear_backend
from backend.documental import listar_documentos, registrar_documento
from backend.seguridad import generar_respaldo_sistema
from backend.pdf_generator import generar_pdf_diagnostico

# Callbacks de exposición JS


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


def mantener_servidor_en_navegacion(page, sockets):
    """Evita la desconexión prematura de Python al cambiar de vista HTML."""
    time.sleep(1.5)
    if not eel._websockets:
        sys.exit(0)


if __name__ == "__main__":
    web_folder = os.path.join(os.path.dirname(__file__), 'web')
    eel.init(web_folder)

    eel.start(
        'views/login.html',
        mode='default',
        size=(1024, 728),
        port=0,
        close_callback=mantener_servidor_en_navegacion
    )
