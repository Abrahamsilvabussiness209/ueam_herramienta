# Inicialización del paquete backend

"""
Módulo principal del backend de la herramienta UEAM.
Gestiona autenticación, diagnóstico, documentos, seguridad y reportes PDF.
"""

from .auth import autenticar_usuario
from .diagnostico import guardar_diagnostico_software
from .documental import listar_documentos, registrar_documento
from .seguridad import generar_respaldo_sistema

__all__ = [
    "autenticar_usuario",
    "guardar_diagnostico_software",
    "listar_documentos",
    "registrar_documento",
    "generar_respaldo_sistema"
]
