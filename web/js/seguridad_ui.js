// Lógica de interfaz para Seguridad de Datos con Llaves Maestras (Admin / Secretaría)

function obtenerSesionActiva() {
    // Revisa las distintas claves posibles usadas en el login del sistema
    const posiblesClaves = ["rol", "usuario", "perfil", "user", "username", "ueam_rol", "ueam_usuario"];
    for (const k of posiblesClaves) {
        const val = sessionStorage.getItem(k) || localStorage.getItem(k);
        if (val && val.trim() !== "") {
            // Si es un JSON guardado, intentar extraer rol/usuario
            if (val.startsWith("{")) {
                try {
                    const obj = JSON.parse(val);
                    return obj.rol || obj.usuario || obj.nombre || "Secretaría";
                } catch (e) {}
            }
            return val.trim();
        }
    }
    return "Secretaría";
}

document.addEventListener("DOMContentLoaded", () => {
    const sesion = obtenerSesionActiva();
    const rolNorm = sesion.toLowerCase();

    // 1. Bloqueo estricto para Estudiante
    if (rolNorm.includes("estudiante")) {
        alert("Acceso Restringido: El perfil Estudiante solo tiene autorización para el módulo de Mantenimiento Lógico y Diagnóstico.");
        window.location.href = "/views/dashboard.html";
        return;
    }

    const nombreMostrar = rolNorm.includes("secretar") ? "Secretaría" : (rolNorm.includes("admin") ? "Administrador" : sesion);

    const badgePerfil = document.getElementById("badge-perfil-activo");
    if (badgePerfil) {
        badgePerfil.textContent = `Sesión Autorizada: ${nombreMostrar} (Acceso a Bóveda Activo)`;
    }

    cargarBitacoraSeguridad();

    // 2. Cifrado con Llave Maestra
    const form = document.getElementById("seguridad-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const fileInput = document.getElementById("seg_archivo");
            const claveInput = document.getElementById("seg_clave");

            if (!fileInput.files || !fileInput.files[0]) {
                alert("Por favor seleccione un archivo digital.");
                return;
            }

            const archivo = fileInput.files[0];
            const llaveMaestra = claveInput.value;

            const panelProgreso = document.getElementById("panel-progreso");
            const barra = document.getElementById("barra-progreso");
            const resultadoBox = document.getElementById("resultado-hash-box");

            panelProgreso.style.display = "block";
            resultadoBox.style.display = "none";
            barra.style.backgroundColor = "#27ae60";
            barra.style.width = "35%";
            barra.textContent = "35% - Validando Llave Maestra y Hash SHA-256...";

            const reader = new FileReader();
            reader.onload = function(event) {
                const base64String = event.target.result.split(",")[1];

                barra.style.width = "70%";
                barra.textContent = "70% - Cifrando bytes en Bóveda...";

                eel.proteger_archivo_seguridad(archivo.name, base64String, llaveMaestra, nombreMostrar)((res) => {
                    if (res && res.exito) {
                        barra.style.width = "100%";
                        barra.textContent = "100% - ¡Resguardado en Bóveda!";

                        document.getElementById("out-nombre-enc").textContent = res.archivo_protegido;
                        document.getElementById("out-codigo-hash").textContent = res.hash;
                        resultadoBox.style.display = "block";

                        form.reset();
                        cargarBitacoraSeguridad();
                    } else {
                        barra.style.backgroundColor = "#e74c3c";
                        barra.textContent = "Acceso Denegado / Error";
                        alert(res ? res.mensaje : "No se pudo procesar el archivo.");
                    }
                });
            };
            reader.readAsDataURL(archivo);
        });
    }

    // 3. Respaldo ZIP general
    const btnBackup = document.getElementById("btn-generar-backup");
    if (btnBackup) {
        btnBackup.addEventListener("click", async () => {
            try {
                const res = await eel.generar_respaldo_sistema()();
                if (res && res.exito) {
                    alert("✅ " + res.mensaje);
                } else {
                    alert("❌ Error generando respaldo: " + (res ? res.mensaje : "Desconocido"));
                }
            } catch (err) {
                console.error("Error en respaldo ZIP:", err);
            }
        });
    }
});

// 4. Listar Bóveda Segura y habilitar Descifrado
function cargarBitacoraSeguridad() {
    const tbody = document.getElementById("tabla-bitacora-body");
    if (!tbody) return;

    eel.listar_bitacora_seguridad()((res) => {
        tbody.innerHTML = "";

        if (!res || !res.exito || !res.registros || res.registros.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #7f8c8d;">No hay archivos resguardados en la bóveda todavía.</td></tr>`;
            return;
        }

        res.registros.forEach((reg) => {
            const hashCorto = reg.hash_sha256 ? reg.hash_sha256.substring(0, 12) + "..." : "N/A";
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${reg.id}</td>
                <td><strong>${reg.archivo_original}</strong><br><small style="color:#7f8c8d;">${reg.fecha_hora}</small></td>
                <td><span style="color: #2980b9; font-weight: 600;">🔒 ${reg.archivo_protegido}</span></td>
                <td><code title="${reg.hash_sha256}" style="background:#edf2f7; padding:2px 5px; border-radius:4px; font-size:0.75rem;">${hashCorto}</code></td>
                <td><span style="color: #27ae60; font-weight: 600;">${reg.usuario}</span></td>
                <td>
                    <button type="button" class="btn-descifrar" onclick="solicitarDescifrado('${reg.archivo_protegido}', '${reg.archivo_original}')">
                        🔓 Descifrar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    });
}

function solicitarDescifrado(nombreProtegido, nombreOriginal) {
    const sesion = obtenerSesionActiva();
    const llave = prompt(`Ingrese su Llave Maestra (${sesion}) para descifrar y descargar "${nombreOriginal}":`);
    
    if (!llave) return;

    eel.descifrar_y_recuperar_archivo(nombreProtegido, nombreOriginal, llave, sesion)((res) => {
        if (res && res.exito) {
            alert(`✅ ${res.mensaje}`);
        } else {
            alert(`❌ ${res ? res.mensaje : "Error al descifrar el archivo."}`);
        }
    });
}