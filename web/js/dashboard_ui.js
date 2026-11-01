// Control de roles, permisos y cierre de sesión seguro en el Dashboard

document.addEventListener("DOMContentLoaded", () => {
    const btnCerrarSesion = document.getElementById("btn-cerrar-sesion");
    const infoRol = document.getElementById("info-rol");

    const cardDocumental = document.getElementById("card-documental");
    const cardSeguridad = document.getElementById("card-seguridad");
    const cardCodigo = document.getElementById("card-codigo");

    const rolUsuario = sessionStorage.getItem("usuario_rol") || "Estudiante";
    const nombreUsuario = sessionStorage.getItem("usuario_nombre") || "Usuario";

    const rol = rolUsuario.toLowerCase();

    // Restricción estricta según el rol
    if (rol === "estudiante") {
        if (infoRol) infoRol.innerText = "Perfil: Estudiante (Acceso Restringido)";
        
        // Estudiante SOLO ve el módulo de Diagnóstico
        if (cardDocumental) cardDocumental.style.display = "none";
        if (cardSeguridad) cardSeguridad.style.display = "none";
        if (cardCodigo) cardCodigo.style.display = "none";

    } else if (rol === "secretaria") {
        if (infoRol) infoRol.innerText = `${nombreUsuario} | Rol: Secretaría`;
        if (cardCodigo) cardCodigo.style.display = "none";
    } else {
        if (infoRol) infoRol.innerText = `${nombreUsuario} | Rol: Administrador`;
    }

    // Cierre de sesión limpio hacia la bienvenida
    if (btnCerrarSesion) {
        btnCerrarSesion.addEventListener("click", (e) => {
            e.preventDefault();
            sessionStorage.clear();
            window.location.href = "/views/login.html";
        });
    }

    const btnVerCodigo = document.getElementById("btn-ver-codigo");
    if (btnVerCodigo) {
        btnVerCodigo.addEventListener("click", (e) => {
            e.preventDefault();
            if (rol === "estudiante" || rol === "secretaria") {
                alert("Acceso denegado: Función exclusiva para el Administrador.");
            } else {
                alert("Estructura del código fuente en estado óptimo.");
            }
        });
    }
});