# Módulo de seguridad y mantenimiento lógico

import os
import shutil
from datetime import datetime

STORAGE_DIR = os.path.join(os.path.dirname(__file__), '..', 'storage')
BACKUP_DIR = os.path.join(STORAGE_DIR, 'backups')


def generar_respaldo_sistema():
    """Genera un archivo comprimido (.zip) con la copia de todos los datos en storage/."""
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_ueam_{timestamp}"
        destino_zip = os.path.join(BACKUP_DIR, nombre_archivo)

        # Empaquetado zip
        shutil.make_archive(destino_zip, 'zip', STORAGE_DIR)

        return {
            "exito": True,
            "mensaje": f"Respaldo creado correctamente: {nombre_archivo}.zip",
            "archivo": f"{nombre_archivo}.zip"
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error al generar copia de seguridad: {str(e)}"}
