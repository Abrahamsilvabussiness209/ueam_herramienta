// Script principal de la interfaz web

document.addEventListener('DOMContentLoaded', () => {
    // 1. Verificar si existe sesión iniciada
    const sesion = JSON.parse(localStorage.getItem('session_user'));

    if (!sesion) {
        window.location.href = 'login.html';
        return;
    }

    // 2. Colocar nombre y rol en el encabezado
    const userDisplay = document.getElementById('user-display');
    if (userDisplay) {
        userDisplay.textContent = `${sesion.nombre} | Rol: ${sesion.rol}`;
    }

    // 3. Extraer permisos
    const permisos = sesion.permisos || [];

    // 4. Mostrar u ocultar tarjetas según los IDs definidos en el HTML
    mostrarUOcultar('card-diagnostico', permisos.includes('diagnostico'));
    mostrarUOcultar('card-documental', permisos.includes('documental'));
    mostrarUOcultar('card-seguridad', permisos.includes('seguridad'));
    mostrarUOcultar('card-codigo', permisos.includes('codigo'));
});

function mostrarUOcultar(idElemento, visibilidad) {
    const elemento = document.getElementById(idElemento);
    if (elemento) {
        elemento.style.display = visibilidad ? 'block' : 'none';
    }
}

function cerrarSesion() {
    localStorage.removeItem('session_user');
    window.location.href = 'login.html';
}