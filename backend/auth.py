# Módulo de autenticación y sesiones

import json
import os

# Ruta dinámica hacia el archivo de usuarios planos
USUARIOS_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'storage', 'system_data', 'usuarios.json'
)


def cargar_usuarios():
    """Lee y retorna la lista de usuarios desde el archivo JSON plano."""
    if not os.path.exists(USUARIOS_FILE):
        return []
    with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def guardar_usuarios_seguro(usuarios):
    """Guarda los usuarios usando un archivo temporal (.tmp)."""
    temp_file = f"{USUARIOS_FILE}.tmp"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    os.replace(temp_file, USUARIOS_FILE)


def autenticar_usuario(username: str, password: str = ""):
    """Valida las credenciales ingresadas.

    Permite ingreso directo sin contraseña únicamente para el rol Estudiante.
    """
    usuarios = cargar_usuarios()

    for user in usuarios:
        # 1. Comprobar coincidencia del nombre de usuario
        if user.get("usuario", "").lower() == username.lower():

            # Caso 1: Perfil Estudiante (Acceso directo libre sin contraseña)
            if user.get("rol") == "Estudiante":
                return {
                    "exito": True,
                    "mensaje": "Acceso concedido como Estudiante",
                    "usuario": {
                        "id": user.get("id"),
                        "nombre": user.get("nombre"),
                        "rol": user.get("rol"),
                        "permisos": user.get("permisos", ["diagnostico"])
                    }
                }

# Caso 2: Perfiles protegidos (Admin, Secretaría) con clave válida
            elif user.get("password_hash") == password and password != "":
                return {
                    "exito": True,
                    "mensaje": "Inicio de sesión exitoso",
                    "usuario": {
                        "id": user.get("id"),
                        "nombre": user.get("nombre"),
                        "rol": user.get("rol"),
                        "permisos": user.get("permisos", [])
                    }
                }

# Caso 3: Usuario encontrado pero contraseña inválida
            else:
                return {
                    "exito": False,
                    "mensaje": "Contraseña incorrecta"
                }

# Si no hubo ninguna coincidencia tras recorrer toda la lista
    return {
        "exito": False,
        "mensaje": "Usuario no encontrado"
    }
