# Módulo de autenticación y sesiones

import json
import os

# Ruta dinámica hacia el archivo de usuarios planos
USUARIOS_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'storage', 'system_data', 'usuarios.json'
)

def inicializar_usuarios_por_defecto():
    """Crea la estructura de usuarios por defecto si el archivo no existe o está vacío."""
    usuarios_default = [
        {
            "id": 1,
            "usuario": "estudiante",
            "nombre": "Estudiante UEAM",
            "rol": "Estudiante",
            "password_hash": "",
            "permisos": ["diagnostico"]
        },
        {
            "id": 2,
            "usuario": "secretaria",
            "nombre": "Secretaría UEAM",
            "rol": "Secretaria",
            "password_hash": "secretaria123",
            "permisos": ["diagnostico", "documental"]
        },
        {
            "id": 3,
            "usuario": "admin",
            "nombre": "Administrador Principal",
            "rol": "Administrador",
            "password_hash": "admin123",
            "permisos": ["diagnostico", "documental", "seguridad", "codigo"]
        }
    ]
    
    os.makedirs(os.path.dirname(USUARIOS_FILE), exist_ok=True)
    with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios_default, f, indent=4, ensure_ascii=False)
    return usuarios_default


def cargar_usuarios():
    """Lee y retorna la lista de usuarios desde el archivo JSON plano."""
    if not os.path.exists(USUARIOS_FILE):
        return inicializar_usuarios_por_defecto()
    try:
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                return inicializar_usuarios_por_defecto()
            return data
    except Exception:
        return inicializar_usuarios_por_defecto()


def guardar_usuarios_seguro(usuarios):
    """Guarda los usuarios usando un archivo temporal (.tmp)."""
    os.makedirs(os.path.dirname(USUARIOS_FILE), exist_ok=True)
    temp_file = f"{USUARIOS_FILE}.tmp"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    os.replace(temp_file, USUARIOS_FILE)


def autenticar_usuario(username: str, password: str = ""):
    """Valida las credenciales ingresadas.

    Permite ingreso directo sin contraseña únicamente para el rol Estudiante.
    """
    usuarios = cargar_usuarios()
    user_buscado = str(username).strip().lower()
    pass_ingresada = str(password).strip()

    for user in usuarios:
        db_username = str(user.get("usuario", "")).strip().lower()
        db_rol = str(user.get("rol", "")).strip()

        # 1. Comprobar coincidencia del nombre de usuario o rol Estudiante directo
        if db_username == user_buscado or (user_buscado == "estudiante" and db_rol == "Estudiante"):

            # Caso 1: Perfil Estudiante (Acceso directo libre sin contraseña)
            if db_rol == "Estudiante":
                return {
                    "exito": True,
                    "mensaje": "Acceso concedido como Estudiante",
                    "rol": "Estudiante",
                    "nombre": user.get("nombre", "Estudiante UEAM"),
                    "usuario": {
                        "id": user.get("id", 1),
                        "nombre": user.get("nombre", "Estudiante UEAM"),
                        "rol": "Estudiante",
                        "permisos": user.get("permisos", ["diagnostico"])
                    }
                }

            # Caso 2: Perfiles protegidos (Admin, Secretaría) con clave válida
            db_pass = str(user.get("password_hash", ""))
            if db_pass == pass_ingresada and pass_ingresada != "":
                return {
                    "exito": True,
                    "mensaje": "Inicio de sesión exitoso",
                    "rol": db_rol,
                    "nombre": user.get("nombre", db_rol),
                    "usuario": {
                        "id": user.get("id", 2),
                        "nombre": user.get("nombre", db_rol),
                        "rol": db_rol,
                        "permisos": user.get("permisos", [])
                    }
                }
            else:
                # Caso 3: Usuario encontrado pero contraseña inválida
                return {
                    "exito": False,
                    "mensaje": "Contraseña incorrecta"
                }

    # Si no hubo ninguna coincidencia tras recorrer toda la lista
    return {
        "exito": False,
        "mensaje": "Usuario no encontrado"
    }
