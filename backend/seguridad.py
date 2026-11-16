# Módulo de seguridad de datos, bóveda criptográfica y respaldos

import os
import json
import base64
import shutil
import hashlib
from datetime import datetime
import eel

STORAGE_DIR = os.path.join(os.path.dirname(__file__), '..', 'storage')
BACKUP_DIR = os.path.join(STORAGE_DIR, 'backups')
BOVEDA_DIR = os.path.join(STORAGE_DIR, 'boveda_segura')
META_DIR = os.path.join(STORAGE_DIR, 'system_data')
BITACORA_FILE = os.path.join(META_DIR, 'bitacora_seguridad.json')

# Llaves Maestras institucionales por rol
LLAVES_MAESTRAS = {
    "admin": "UEAM-ADMIN-2026",
    "administrador": "UEAM-ADMIN-2026",
    "secretaria": "UEAM-SEC-2026",
    "secretaría": "UEAM-SEC-2026"
}

LLAVE_INTERNA_BOVEDA = "UEAM_BOVEDA_MAESTRA_LIBERTADOR_2026_SECURE_KEY"


def asegurar_directorios_seguridad():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(BOVEDA_DIR, exist_ok=True)
    os.makedirs(META_DIR, exist_ok=True)


def _identificar_perfil_por_llave(llave_ingresada: str, usuario_sesion: str) -> str:
    """Determina con precisión si la operación la realizó Secretaría o Administrador."""
    llave_limpia = (llave_ingresada or "").strip()
    if llave_limpia == "UEAM-SEC-2026":
        return "Secretaría"
    if llave_limpia == "UEAM-ADMIN-2026":
        return "Administrador"
    
    sesion_norm = (usuario_sesion or "").strip().lower()
    if "secretar" in sesion_norm:
        return "Secretaría"
    return "Administrador"


def _validar_llave_maestra(llave_ingresada: str) -> bool:
    llave_limpia = (llave_ingresada or "").strip()
    return llave_limpia in LLAVES_MAESTRAS.values()


def _procesar_bytes_simetrico(datos_bytes: bytes) -> bytes:
    llave = hashlib.sha256(LLAVE_INTERNA_BOVEDA.encode('utf-8')).digest()
    llave_len = len(llave)
    return bytes([b ^ llave[i % llave_len] for i, b in enumerate(datos_bytes)])


@eel.expose
def generar_respaldo_sistema():
    """Genera un archivo comprimido (.zip) con la copia de todos los datos en storage/."""
    try:
        asegurar_directorios_seguridad()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_ueam_{timestamp}"
        destino_zip = os.path.join(BACKUP_DIR, nombre_archivo)

        shutil.make_archive(destino_zip, 'zip', STORAGE_DIR)

        return {
            "exito": True,
            "mensaje": f"Respaldo creado correctamente: {nombre_archivo}.zip",
            "archivo": f"{nombre_archivo}.zip",
            "ruta": f"{destino_zip}.zip"
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error al generar copia de seguridad: {str(e)}"}


@eel.expose
def proteger_archivo_seguridad(nombre_archivo: str, contenido_base64: str, llave_maestra: str, usuario: str):
    """Calcula Hash SHA-256, cifra bytes (.ueam_enc) y registra en bitácora JSON."""
    asegurar_directorios_seguridad()

    if not _validar_llave_maestra(llave_maestra):
        return {
            "exito": False,
            "mensaje": "Acceso denegado: Llave Maestra incorrecta o perfil sin autorización (solo Admin / Secretaría)."
        }

    try:
        perfil_real = _identificar_perfil_por_llave(llave_maestra, usuario)
        datos_originales = base64.b64decode(contenido_base64)
        huella_hash = hashlib.sha256(datos_originales).hexdigest()
        datos_cifrados = _procesar_bytes_simetrico(datos_originales)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_protegido = f"{nombre_archivo}_{timestamp}.ueam_enc"
        ruta_protegida = os.path.join(BOVEDA_DIR, nombre_protegido)

        with open(ruta_protegida, "wb") as f:
            f.write(datos_cifrados)

        bitacora = []
        if os.path.exists(BITACORA_FILE):
            with open(BITACORA_FILE, "r", encoding="utf-8") as f:
                try:
                    bitacora = json.load(f)
                except json.JSONDecodeError:
                    bitacora = []

        nuevo_registro = {
            "id": len(bitacora) + 1,
            "archivo_original": nombre_archivo,
            "archivo_protegido": nombre_protegido,
            "hash_sha256": huella_hash,
            "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usuario": perfil_real
        }
        bitacora.append(nuevo_registro)

        temp_file = f"{BITACORA_FILE}.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(bitacora, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, BITACORA_FILE)

        return {
            "exito": True,
            "archivo_protegido": nombre_protegido,
            "hash": huella_hash,
            "ruta": ruta_protegida
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error criptográfico: {str(e)}"}


@eel.expose
def descifrar_y_recuperar_archivo(nombre_protegido: str, nombre_original: str, llave_maestra: str, usuario: str):
    """Descifra un archivo de la bóveda con la Llave Maestra y lo guarda en Descargas."""
    if not _validar_llave_maestra(llave_maestra):
        return {
            "exito": False,
            "mensaje": "Llave Maestra inválida. No tiene autorización para descifrar archivos."
        }

    ruta_boveda = os.path.join(BOVEDA_DIR, nombre_protegido)
    if not os.path.exists(ruta_boveda):
        return {"exito": False, "mensaje": "El archivo protegido no existe en la bóveda."}

    try:
        with open(ruta_boveda, "rb") as f:
            datos_cifrados = f.read()

        datos_recuperados = _procesar_bytes_simetrico(datos_cifrados)

        descargas_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(descargas_dir, exist_ok=True)
        ruta_salida = os.path.join(descargas_dir, f"DESCIFRADO_{nombre_original}")

        with open(ruta_salida, "wb") as f:
            f.write(datos_recuperados)

        return {
            "exito": True,
            "mensaje": f"Archivo descifrado con éxito y guardado en Descargas como: DESCIFRADO_{nombre_original}",
            "ruta": ruta_salida
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error al descifrar: {str(e)}"}


@eel.expose
def listar_bitacora_seguridad():
    """Retorna los registros de la bitácora digital JSON."""
    asegurar_directorios_seguridad()
    if not os.path.exists(BITACORA_FILE):
        return {"exito": True, "registros": []}

    try:
        with open(BITACORA_FILE, "r", encoding="utf-8") as f:
            registros = json.load(f)
        return {"exito": True, "registros": registros}
    except Exception as e:
        return {"exito": False, "mensaje": str(e)}
