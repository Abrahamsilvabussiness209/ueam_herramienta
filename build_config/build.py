import os
import subprocess
import sys


def construir_ejecutable():
    print("=== Iniciando proceso de empaquetado UEAM ===")


# Directorio llamando al os de cadda pc

base_dir = os.path.dirname(os.path.abspath(__file__))
web_dir = os.path.join(base_dir, 'web')
main_script = os.path.join(base_dir, 'main.py')


# Comando de PyInstaller para compilar Eel con soporte para la carpeta 'web'

comando = [
 sys.executable, "-m", "PyInstaller",
 "--noconfirm",
 "--onedir",             # Genera carpeta con dependencias (o '--onefile' para archivo único)
 "--windowed",           # Sin ventana de consola
 "--name=UEAM_Sistema",
 f"--add-data={web_dir}{os.pathsep}web",  # Incluye la carpeta del frontend
 main_script
    ]

try:
    subprocess.run(comando, check=True)
    print("\n=== Empaquetado completado con éxito. Revisa la carpeta 'dist/' ===")
except subprocess.CalledProcessError as e:
    print(f"\n[Error] Falló la compilación: {e}")

if __name__ == '__main__':
    construir_ejecutable()
