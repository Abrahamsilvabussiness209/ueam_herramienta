// Script principal de la interfaz web

// Lógica de interfaz para Seguridad

document.addEventListener("DOMContentLoaded", () => {
    const btnBackup = document.getElementById("btn-generar-backup");

    if (btnBackup) {
        btnBackup.addEventListener("click", async () => {
            try {
                let res;
                if (typeof eel !== "undefined") {
                    res = await eel.generar_backup()();
                } else {
                    const response = await fetch("/api/seguridad/backup", { method: "POST" });
                    res = await response.json();
                }

                if (res.exito) {
                    alert("Respaldo creado con éxito en: " + res.ruta);
                } else {
                    alert("Error generando respaldo: " + res.mensaje);
                }
            } catch (err) {
                console.error("Error en módulo de seguridad:", err);
            }
        });
    }
});