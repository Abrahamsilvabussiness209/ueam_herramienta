# Módulo de autenticación y sesiones

import json
import os

USUARIOS_FILE = os.path.join(os.path.dirname(__file__), '..', 'storage', 'system_data', 'usuario.json')


# Modulo de carga los usuarios almacenados en los archivos json
def cargar_usuarios():
   """Lee el archivo json de Usuarios"""
   if not os.path.exists(USUARIOS_FILE):
                              return[]
   with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
                              return json.load(f)


# Modulo de autenticacion de los usuarios almacenados en archivos json
def autenticar_usuario(username, password=""):
                              """
                              Valida las credenciales ingresadas.
                              Permite ingreso directo sin contraseña únicamente para el rol Estudiante.
                              """
                              usuarios = cargar_usuarios()
                              for user in usuarios:
                                                            # En el caso de los Estudiantes (Acceso libre sin contraseña)
                                                            if user ["rol"] == "Estudiante":
                                                                                          return {
                                                                                                                        "exito": True,
                                                                                                                        "mensaje": "Acceso concedido como Estudiante",
                                                                                                                        "usuario": {
                                                                                                                                                      "id": user["id"],
                                                                                                                                                      "nombre": user["nombre"],
                                                                                                                                                      "rol": user["rol"],
                                                                                                                                                      "permisos": user["permisos"],
                                                                                                                        }
                                                                                          }
                                                            # Caso Admin / Tecnico-Secretaria (Requiere contraseña)
                                                            elif user["password_hash"] == password and password != "":
                                                             return {
                                                                                          "exito": True,
                                                                                          "mensaje": "Inicio de sesión exitoso",
                                                                                          "usuario": {
                                                                                                                        "id": user["id"],
                                                                                                                        "nombre": user["nombre"],
                                                                                                                        "rol": user["rol"],
                                                                                                                        "permisos": user["permisos"]
                                                                                          }
                                                            }
                                                            else:
                                                             return {"exito": False, "mensaje": "Contraseña incorrecta"}

                                                            return {"exito": False, "mensaje": "Usuario no encontrado"}