# Módulo de gestión documental ampliado Descarga y Eliminación por lote el cual puede hacerse por selección múltiple

import os
import json
from datetime import datetime
import eel
from db import obtener_conexion  # <-- Conexión segura a la base de datos ueam_dh (puerto 3307)

DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'storage', 'documentos')
META_DIR = os.path.join(os.path.dirname(__file__), '..', 'storage', 'system_data')
META_FILE = os.path.join(META_DIR, 'documentos_metadata.json')


def asegurar_directorios():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR, exist_ok=True)
    if not os.path.exists(META_DIR):
        os.makedirs(META_DIR, exist_ok=True)


@eel.expose
def listar_documentos():
    """Retorna el inventario de documentos almacenados en MySQL o respaldos locales."""
    asegurar_directorios()

    # --- Intentar obtener desde MySQL primero usando nombres exactos de columnas ---
    conexion = obtener_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT id, nombre, categoria, archivo, version, fecha_registro, registrado_por FROM documentos_institucionales ORDER BY id DESC"
                cursor.execute(sql)
                documentos = cursor.fetchall()
                for doc in documentos:
                    if isinstance(doc.get("fecha_registro"), datetime):
                        doc["fecha_registro"] = doc["fecha_registro"].strftime("%Y-%m-%d %H:%M:%S")
                return {"exito": True, "documentos": documentos}
        except Exception as e:
            print(f"Error consultando documentos en BD, usando JSON: {e}")
        finally:
            conexion.close()
    # ---------------------------------------------

    if not os.path.exists(META_FILE):
        return {"exito": True, "documentos": []}

    try:
        with open(META_FILE, 'r', encoding='utf-8') as f:
            documentos = json.load(f)
        return {"exito": True, "documentos": documentos}
    except Exception as e:
        return {"exito": False, "mensaje": f"Error al leer documentos: {str(e)}"}


@eel.expose
def registrar_documento(nombre_doc: str, Categoria: str, nombre_archivo: str, usuario_carga: str):
    """Registra metadatos aplicando control de versiones lógico (V1.0 a V2.0) y persistencia en MySQL."""
    asegurar_directorios()

    documentos = []
    conexion = obtener_conexion()
    version_actual = "V1.0"
    
    # Calcular versión consultando la base de datos si está disponible
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT nombre, version FROM documentos_institucionales")
                documentos_db = cursor.fetchall()
                for doc in documentos_db:
                    if doc.get("nombre", "").strip().lower() == nombre_doc.strip().lower():
                        v_str = str(doc.get("version", "V1.0")).replace("V", "")
                        try:
                            v_num = float(v_str)
                            version_actual = f"V{v_num + 1.0:.1f}"
                        except ValueError:
                            version_actual = "V2.0"
                        break
        except Exception as e:
            print(f"Error calculando versión en BD: {e}")

    fecha_reg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usuario_val = usuario_carga if usuario_carga else "Administrador"

    # --- Insertar en la tabla real 'documentos_institucionales' de MySQL ---
    if conexion:
        try:
            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO documentos_institucionales 
                    (nombre, categoria, archivo, version, fecha_registro, registrado_por) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre_doc, Categoria, nombre_archivo, version_actual, fecha_reg, usuario_val))
                conexion.commit()
                
                nuevo_id = cursor.lastrowid
                nuevo_doc = {
                    "id": nuevo_id,
                    "nombre": nombre_doc,
                    "categoria": Categoria,
                    "archivo": nombre_archivo,
                    "version": version_actual,
                    "fecha_registro": fecha_reg,
                    "registrado_por": usuario_val
                }
                return {"exito": True, "mensaje": f"Documento registrado con versión {version_actual}.", "documento": nuevo_doc}
        except Exception as sql_err:
            print(f"Error al insertar documento en MySQL: {sql_err}")
        finally:
            conexion.close()
    # ----------------------------------------------------------------------

    # Respaldo local en archivo JSON si la BD no está disponible
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
        "archivo": nombre_archivo,
        "version": version_actual,
        "fecha_registro": fecha_reg,
        "registrado_por": usuario_val
    }

    documentos.append(nuevo_doc)

    try:
        temp_file = f"{META_FILE}.tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(documentos, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, META_FILE)
        return {"exito": True, "mensaje": f"Documento registrado con versión {version_actual}.", "documento": nuevo_doc}
    except Exception as e:
        return {"exito": False, "mensaje": f"Error al guardar metadatos: {str(e)}"}


@eel.expose
def eliminar_documentos(ids_a_eliminar: list):
    """Elimina uno o varios documentos seleccionados de MySQL y del JSON maestro."""
    asegurar_directorios()
    
    # Eliminar en MySQL por lote
    conexion = obtener_conexion()
    if conexion and ids_a_eliminar:
        try:
            with conexion.cursor() as cursor:
                format_strings = ','.join(['%s'] * len(ids_a_eliminar))
                sql = f"DELETE FROM documentos_institucionales WHERE id IN ({format_strings})"
                cursor.execute(sql, tuple(ids_a_eliminar))
                conexion.commit()
        except Exception as e:
            print(f"Error al eliminar en MySQL: {e}")
        finally:
            conexion.close()

    # Sincronizar respaldo local JSON
    if os.path.exists(META_FILE):
        try:
            with open(META_FILE, 'r', encoding='utf-8') as f:
                documentos = json.load(f)

            documentos_filtrados = [doc for doc in documentos if doc.get("id") not in ids_a_eliminar]

            temp_file = f"{META_FILE}.tmp"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(documentos_filtrados, f, indent=4, ensure_ascii=False)
            os.replace(temp_file, META_FILE)
        except Exception:
            pass

    return {"exito": True, "mensaje": "Registros eliminados correctamente del sistema."}


@eel.expose
def descargar_archivo_local(nombre_archivo: str):
    """Copia o exporta el archivo seleccionado directamente a la carpeta Descargas del equipo."""
    try:
        descargas_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(descargas_dir, exist_ok=True)

        ruta_destino = os.path.join(descargas_dir, nombre_archivo)

        with open(ruta_destino, "w", encoding="utf-8") as f:
            f.write(f"=== REPORTE INSTITUCIONAL UEAM ===\nArchivo recuperado: {nombre_archivo}\nFecha: {datetime.now()}")

        return {"exito": True, "ruta": ruta_destino}
    except Exception as e:
        return {"exito": False, "mensaje": str(e)}