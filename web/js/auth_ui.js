// Lógica de autenticación, sincronización de roles y verificación matemática con el backend

document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("btn-login");
    const roleRadios = document.querySelectorAll('input[name="rol"]');
    const passGroup = document.getElementById("pass-group");
    const userGroup = document.getElementById("user-group");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const roleNote = document.getElementById("role-note");
    const mathQuestion = document.getElementById("math-question");
    const mathAnswer = document.getElementById("math-answer");

    // Generar operación matemática aleatoria al cargar la página
    let num1 = Math.floor(Math.random() * 8) + 2; // Número entre 2 y 9
    let num2 = Math.floor(Math.random() * 6) + 1; // Número entre 1 y 6
    let resultadoCorrecto = num1 + num2;

    if (mathQuestion) {
        mathQuestion.innerText = `Verificación de seguridad: ¿Cuánto es ${num1} + ${num2}?`;
    }

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

    // Acción principal del botón de ingreso con validación matemática
    if (btnLogin) {
        btnLogin.addEventListener("click", (e) => {
            e.preventDefault();

            // Validar respuesta de la verificación matemática
            const respuestaUsuario = parseInt(mathAnswer ? mathAnswer.value.trim() : "");
            if (isNaN(respuestaUsuario) || respuestaUsuario !== resultadoCorrecto) {
                alert("⚠️ Error de seguridad: La respuesta de la verificación matemática es incorrecta. Inténtalo de nuevo.");
                if (mathAnswer) {
                    mathAnswer.value = "";
                    mathAnswer.focus();
                }
                return; // Detiene el acceso inmediatamente si falla
            }

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