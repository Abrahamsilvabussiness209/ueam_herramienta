// Lógica de interfaz para Autenticación

document.addEventListener('DOMContentLoaded', () => {
    const formLogin = document.getElementById('form-login');
    const radioEstudiante = document.getElementById('radio-estudiante');
    const radioTecnico = document.getElementById('radio-tecnico');
    const radioAdmin = document.getElementById('radio-admin');
    
    const groupUsuario = document.getElementById('group-usuario');
    const groupPassword = document.getElementById('group-password');
    const infoEstudiante = document.getElementById('info-estudiante');
    const btnIngresar = document.getElementById('btn-ingresar');
    const errorMsg = document.getElementById('error-message');

    // Cambiar la vista del formulario dinámicamente según el rol seleccionado
    function actualizarFormulario() {
        if (radioEstudiante && radioEstudiante.checked) {
            if (groupUsuario) groupUsuario.style.display = 'none';
            if (groupPassword) groupPassword.style.display = 'none';
            if (infoEstudiante) infoEstudiante.style.display = 'block';
            if (btnIngresar) btnIngresar.textContent = 'Ingresar como Estudiante';
        } else {
            if (groupUsuario) groupUsuario.style.display = 'block';
            if (groupPassword) groupPassword.style.display = 'block';
            if (infoEstudiante) infoEstudiante.style.display = 'none';
            if (btnIngresar) btnIngresar.textContent = 'Iniciar Sesión';
        }
        if (errorMsg) errorMsg.textContent = '';
    }

    // Escuchar cambios de opción en los radio buttons
    if (radioEstudiante) radioEstudiante.addEventListener('change', actualizarFormulario);
    if (radioTecnico) radioTecnico.addEventListener('change', actualizarFormulario);
    if (radioAdmin) radioAdmin.addEventListener('change', actualizarFormulario);

    // Inicializar el estado visual del formulario
    actualizarFormulario();

    // Manejo del envío del formulario
    if (formLogin) {
        formLogin.addEventListener('submit', (e) => {
            e.preventDefault();

            let sesionData = null;

            if (radioEstudiante && radioEstudiante.checked) {
                // Perfil Estudiante: Sin contraseña (Acceso directo únicamente a Diagnóstico)
                sesionData = {
                    usuario: "estudiante",
                    nombre: "Estudiante UEAM",
                    rol: "Estudiante",
                    permisos: ["diagnostico"]
                };
            } else {
                // Perfiles Admin y Técnico/Secretaría
                const inputUser = document.getElementById('input-usuario');
                const inputPass = document.getElementById('input-password');

                const userVal = inputUser ? inputUser.value.trim() : '';
                const passVal = inputPass ? inputPass.value.trim() : '';

                if (!userVal || !passVal) {
                    if (errorMsg) errorMsg.textContent = 'Por favor complete todos los campos.';
                    return;
                }

                // Validación local de prueba
                if (userVal === "admin" && passVal === "admin123") {
                    sesionData = {
                        usuario: "admin",
                        nombre: "Administrador Sistema",
                        rol: "Admin",
                        permisos: ["diagnostico", "documental", "seguridad", "codigo"]
                    };
                } else if (userVal === "tecnico_secretaria" && passVal === "user123") {
                    sesionData = {
                        usuario: "tecnico_secretaria",
                        nombre: "Técnico / Secretaría",
                        rol: "TecnicoSecretaria",
                        permisos: ["diagnostico", "documental", "seguridad"]
                    };
                } else {
                    if (errorMsg) errorMsg.textContent = 'Usuario o contraseña incorrectos.';
                    return;
                }
            }

            // Guardar datos en el almacenamiento local del navegador
            localStorage.setItem('session_user', JSON.stringify(sesionData));

            // Redireccionar al Dashboard principal
            window.location.href = 'dashboard.html';
        });
    }
});