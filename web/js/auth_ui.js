// Lógica de autenticación y sincronización de roles con el backend

document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("btn-login");
    const roleRadios = document.querySelectorAll('input[name="rol"]');
    const passGroup = document.getElementById("pass-group");
    const userGroup = document.getElementById("user-group");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const roleNote = document.getElementById("role-note");

    // Cambiar comportamiento visual según el radio button seleccionado
    roleRadios.forEach(radio => {
        radio.addEventListener("change", (e) => {
            const selectedRole = e.target.value;
            if (selectedRole === "Estudiante") {
                if (passGroup) passGroup.style.display = "none";
                if (userGroup) userGroup.style.display = "none";
                if (roleNote) roleNote.innerText = "💡 El perfil de Estudiante no requiere contraseña y sólo tiene acceso al Módulo de Diagnóstico.";
                if (usernameInput) usernameInput.value = "Estudiante";
                if (btnLogin) btnLogin.innerText = "Ingresar como Estudiante";
            } else if (selectedRole === "Secretaria") {
                if (passGroup) passGroup.style.display = "block";
                if (userGroup) userGroup.style.display = "block";
                if (roleNote) roleNote.innerText = "🔐 Acceso para Secretaría: Gestión Documental y Diagnóstico.";
                if (usernameInput) usernameInput.value = "secretaria";
                if (passwordInput) passwordInput.value = "";
                if (btnLogin) btnLogin.innerText = "Ingresar como Secretaría";
            } else {
                if (passGroup) passGroup.style.display = "block";
                if (userGroup) userGroup.style.display = "block";
                if (roleNote) roleNote.innerText = "⚡ Acceso de Administrador: Control total del sistema.";
                if (usernameInput) usernameInput.value = "admin";
                if (passwordInput) passwordInput.value = "";
                if (btnLogin) btnLogin.innerText = "Ingresar como Administrador";
            }
        });
    });

    // Acción principal del botón de ingreso
    if (btnLogin) {
        btnLogin.addEventListener("click", (e) => {
            e.preventDefault();
            const rolSeleccionado = document.querySelector('input[name="rol"]:checked').value;
            const user = usernameInput ? usernameInput.value.trim() : "Estudiante";
            const pass = passwordInput ? passwordInput.value.trim() : "";

            // Si es estudiante, entra directo sin consultar backend para agilizar
            if (rolSeleccionado === "Estudiante") {
                sessionStorage.setItem("usuario_rol", "Estudiante");
                sessionStorage.setItem("usuario_nombre", "Estudiante UEAM");
                window.location.href = "/views/dashboard.html";
                return;
            }

            // Validación para Secretaría o Administrador mediante Eel
            if (typeof eel !== "undefined" && eel.login_user) {
                eel.login_user(user, pass)((respuesta) => {
                    if (respuesta && respuesta.exito) {
                        sessionStorage.setItem("usuario_rol", respuesta.rol);
                        sessionStorage.setItem("usuario_nombre", respuesta.nombre || user);
                        window.location.href = "/views/dashboard.html";
                    } else {
                        alert("Credenciales incorrectas: " + (respuesta ? respuesta.mensaje : "Error al conectar con el servidor."));
                    }
                });
            } else {
                // Fallback de seguridad en caso de prueba local sin backend activo
                sessionStorage.setItem("usuario_rol", rolSeleccionado);
                sessionStorage.setItem("usuario_nombre", user);
                window.location.href = "/views/dashboard.html";
            }
        });
    }
});