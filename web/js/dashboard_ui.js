// Lógica de control de roles, permisos y navegación del Dashboard

document.addEventListener("DOMContentLoaded", () => {
    const btnCerrarSesion = document.getElementById("btn-cerrar-sesion");
    const infoRol = document.getElementById("info-rol");

    const cardDiagnostico = document.getElementById("card-diagnostico");
    const cardDocumental = document.getElementById("card-documental");
    const cardSeguridad = document.getElementById("card-seguridad");
    const cardCodigo = document.getElementById("card-codigo");


    // Recuperar el rol almacenado en sessionStorage durante el login
    const rolUsuario = sessionStorage.getItem("usuario_rol") || "Estudiante";
    const nombreUsuario = sessionStorage.getItem("usuario_nombre") || "Usuario";


    // Mostrar información en el encabezado según el rol
    const rol = rolUsuario.toLowerCase();
    
    if (rol === "estudiante") {
        if (infoRol) infoRol.innerText = "Perfil: Estudiante (Acceso Restringido)";


        // Restricción estricta solicitada: El estudiante SOLO debe ver el módulo de diagnóstico
        if (cardDocumental) cardDocumental.style.display = "none";
        if (cardSeguridad) cardSeguridad.style.display = "none";
        if (cardCodigo) cardCodigo.style.display = "none";

    } else if (rol === "secretaria") {
        if (infoRol) infoRol.innerText = `${nombreUsuario} | Rol: Secretaría`;
        if (cardCodigo) cardCodigo.style.display = "none"; // Secretaría no ve el código fuente

    } else {
        if (infoRol) infoRol.innerText = `${nombreUsuario} | Rol: Administrador`;
    }


    // Evento de Cerrar Sesión seguro sin bloqueos
    if (btnCerrarSesion) {
        btnCerrarSesion.addEventListener("click", (e) => {
            e.preventDefault();
            sessionStorage.clear();
            // Redirección limpia a la página de bienvenida / login principal
            window.location.href = "login.html";
        });
    }


    // Seguridad adicional para el botón de código fuente (Exclusivo Admin)
    const btnVerCodigo = document.getElementById("btn-ver-codigo");
    if (btnVerCodigo) {
        btnVerCodigo.addEventListener("click", (e) => {
            e.preventDefault();
            if (rolUsuario.toLowerCase() === "estudiante" || rolUsuario.toLowerCase() === "secretaria") {
                alert("Acceso denegado: Esta función es exclusiva para el Administrador.");
            } else {
                alert("Abriendo visor de estructura del código fuente...");
            }
        });
    }
});