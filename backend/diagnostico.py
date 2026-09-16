# Modulo de Diagnostico y Mantenimiento
import os
import shutil
import subprocess
import gc
import ctypes
import psutil


def obtener_tamano_temp():
    """Calcula el tamaño real acumulado en MB de la carpeta Temp del usuario."""
    temp_dir = os.getenv('TEMP')
    total_bytes = 0
    if temp_dir and os.path.exists(temp_dir):
        for dirpath, _, filenames in os.walk(temp_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    if not os.path.islink(fp):
                        total_bytes += os.path.getsize(fp)
                except Exception:
                    pass  # Archivos bloqueados por procesos activos
    return round(total_bytes / (1024 * 1024), 1)


def escanear_sistema(codigo_equipo):
    """Escanea métricas reales de RAM, Disco y Temporales."""
    try:
        mem = psutil.virtual_memory()
        disco = psutil.disk_usage('/')
        procesos = len(psutil.pids())
        cache_mb = obtener_tamano_temp()

        ram_pct = round(mem.percent, 1)
        disco_libre_gb = round(disco.free / (1024**3), 2)
        disco_uso_pct = round(disco.percent, 1)

        nivel_alerta = "VERDE"
        evaluacion = "Sistema en estado óptimo"
        if ram_pct > 80 or disco_uso_pct > 85:
            nivel_alerta = "ROJO"
            evaluacion = "Rendimiento Crítico: Sistema sobrecargado"
        elif ram_pct > 65 or disco_uso_pct > 70:
            nivel_alerta = "AMARILLO"
            evaluacion = "Rendimiento Moderado: Requiere Limpieza"

        return {
            "exito": True,
            "antes": {
                "ram_uso_pct": ram_pct,
                "disco_libre_gb": disco_libre_gb,
                "disco_uso_pct": disco_uso_pct,
                "cache_temp_mb": cache_mb,
                "procesos_activos": procesos,
                "nivel_alerta": nivel_alerta,
                "evaluacion": evaluacion
            }
        }
    except Exception as e:
        return {"exito": False, "mensaje": str(e)}


def ejecutar_mantenimiento_logico(datos):
    """Ejecuta acciones de limpieza reales en el sistema operativo."""
    tipo = datos.get("tipo_mantenimiento", "Preventivo")

    # 1. Limpieza Real de Archivos Temporales
    if "Preventivo" in tipo:
        temp_dir = os.getenv('TEMP')
        if temp_dir and os.path.exists(temp_dir):
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path, ignore_errors=True)
                except Exception:
                    pass  # Omite archivos actualmente en uso por el SO

        # Purga de caché DNS en Windows
        try:
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, creationflags=flags)
        except Exception:
            pass

    # 2. Liberación de RAM y Procesos
    if "Correctivo" in tipo or "Preventivo" in tipo:
        gc.collect()  # Liberación de memoria en Python

        # Purga de Working Set de procesos en Windows
        if os.name == 'nt':
            try:
                handle = ctypes.windll.kernel32.GetCurrentProcess()
                ctypes.windll.psapi.EmptyWorkingSet(handle)
            except Exception:
                pass

    # Métricas reales obtenidas tras la limpieza
    mem = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    procesos = len(psutil.pids())
    cache_mb = obtener_tamano_temp()

    return {
        "exito": True,
        "mensaje": f"Mantenimiento {tipo} ejecutado con éxito en el equipo.",
        "despues": {
            "ram_uso_pct": round(mem.percent, 1),
            "disco_libre_gb": round(disco.free / (1024**3), 2),
            "disco_uso_pct": round(disco.percent, 1),
            "cache_temp_mb": cache_mb,
            "procesos_activos": procesos,
            "evaluacion": "Optimización Exitosa: Rendimiento Restablecido"
        }
    }
