# Módulo de gestión documental

import os
import json
from datetime import datetime

DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'storage', 'documentos')
META_FILE = os.path.join(os.path.dirname(__file__), '..', 'storage', 'system_data', 'documentos_metadata.json')


def asegurar_directorios():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)


def listar_documentos():
    """Retorna el inventario de documentos almacenados localmente."""
    asegurar_directorios()

    if not os.path.exists(META_FILE):
        return {"exito": True, "documentos": []}

    try:
        with open(META_FILE, 'r', encoding='utf-8') as f:
            documentos = json.load(f)
        return {"exito": True, "documentos": documentos}
    except Exception as e:
        return {"exito": False, "mensaje": f"Error al leer documentos: {str(e)}"}


def registrar_documento(nombre_doc: str, Categoria: str, usuario_carga: str):
    """Registra metadatos de un nuevo documento institucional."""
    asegurar_directorios()

    documentos = []
    if os.path.exists(META_FILE):
        with open(META_FILE, 'r', encoding='utf-8') as f:
            try:
                documentos = json.load(f)
            except json.JSONDecodeError:
                documentos = []

    nuevo_doc = {
        "id": len(documentos) + 1,
        "nombre": nombre_doc,
        "categoria": Categoria,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "registrado_por": usuario_carga
    }

    documentos.append(nuevo_doc)

    # Escritura atómica anti-apagones
    temp_file = f"{META_FILE}.tmp"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(documentos, f, indent=4, ensure_ascii=False)
    os.replace(temp_file, META_FILE)

    return {"exito": True, "mensaje": "Documento registrado correctamente.", "documento": nuevo_doc}
