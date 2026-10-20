// Logica de la interfaz de diagnostico optimizada

document.addEventListener("DOMContentLoaded", () => {
    const btnDiagnosticar = document.getElementById("btn-diagnosticar");
    const btnMantenimiento = document.getElementById("btn-mantenimiento");
    const btnExportarPDF = document.getElementById("btn-exportar-pdf");
    const btnGuardar = document.getElementById("btn-guardar");
    const linkVolver = document.getElementById("link-volver");
    const accionesFinales = document.getElementById("acciones-finales");
    const loadingScan = document.getElementById("loading-scan");
    const formMantenimiento = document.getElementById("diagnostico-form");
    
    const codigoInput = document.getElementById("codigo_equipo");
    const sistemaOperativoInput = document.getElementById("sistema_operativo");
    const statusBanner = document.getElementById("status-banner");

    let metricasAntesGlobal = null;
    let datosMantenimientoUltimo = null;

    // Función segura y definitiva para retornar al Dashboard usando la ruta absoluta del servidor local
    function regresarDashboard(e) {
        if (e) e.preventDefault();
        window.location.href = "/views/dashboard.html";
    }

    if (linkVolver) {
        linkVolver.addEventListener("click", regresarDashboard);
    }

    // Escaneo de Métricas (ANTES)
    btnDiagnosticar.addEventListener("click", () => {
        const codigo = codigoInput.value.trim();
        const so = sistemaOperativoInput.value.trim();
        
        if (!codigo || !so) {
            alert("Por favor, ingrese el código del equipo y el sistema operativo.");
            return;
        }

        btnDiagnosticar.style.display = "none";
        loadingScan.style.display = "flex";

        eel.escanear_sistema(codigo)((respuesta) => {
            loadingScan.style.display = "none";

            if (respuesta && respuesta.exito) {
                metricasAntesGlobal = respuesta.antes;
                const m = respuesta.antes;

                const ramFormateada = Number(m.ram_uso_pct).toFixed(1);

                document.getElementById("ram-antes").innerText = `${ramFormateada}%`;
                document.getElementById("disco-antes").innerText = `${m.disco_libre_gb} GB (${m.disco_uso_pct}% usado)`;
                document.getElementById("cache-antes").innerText = `${m.cache_temp_mb} MB`;
                document.getElementById("procesos-antes").innerText = `${m.procesos_activos} procesos`;

                statusBanner.className = `status-alert alert-${m.nivel_alerta.toLowerCase()}`;
                document.getElementById("status-text").innerText = `[ALERTA ${m.nivel_alerta}] ${m.evaluacion}`;

                formMantenimiento.style.display = "block";
                codigoInput.readOnly = true;
                sistemaOperativoInput.readOnly = true;
            } else {
                btnDiagnosticar.style.display = "block";
                alert("Error al escanear: " + (respuesta ? respuesta.mensaje : "Sin respuesta del backend."));
            }
        });
    });

    // Ejecutar Mantenimiento
    btnMantenimiento.addEventListener("click", (e) => {
        e.preventDefault();

        if (!metricasAntesGlobal) {
            alert("Debe realizar el escaneo previo antes de ejecutar el mantenimiento.");
            return;
        }

        btnMantenimiento.disabled = true;
        btnMantenimiento.innerText = "Optimizando sistema y purgando caché...";

        datosMantenimientoUltimo = {
            codigo_equipo: codigoInput.value,
            sistema_operativo: sistemaOperativoInput.value,
            tipo_mantenimiento: document.getElementById("tipo_mantenimiento").value,
            observaciones: document.getElementById("observaciones").value || "Sin observaciones adicionales.",
            metricas_antes: metricasAntesGlobal
        };

        eel.procesar_mantenimiento(datosMantenimientoUltimo)((respuesta) => {
            btnMantenimiento.disabled = false;
            btnMantenimiento.innerText = "Ejecutar Mantenimiento Lógico";

            if (respuesta && respuesta.exito) {
                const d = respuesta.despues;
                const ramDespuesFormateada = Number(d.ram_uso_pct).toFixed(1);

                document.getElementById("ram-despues").innerText = `${ramDespuesFormateada}%`;
                document.getElementById("disco-despues").innerText = `${d.disco_libre_gb} GB (${d.disco_uso_pct}% usado)`;
                document.getElementById("cache-despues").innerText = `${d.cache_temp_mb} MB`;
                document.getElementById("procesos-despues").innerText = `${d.procesos_activos} procesos`;

                statusBanner.className = "status-alert alert-verde";
                document.getElementById("status-text").innerText = `[ALERTA VERDE] ${d.evaluacion}`;

                btnMantenimiento.style.display = "none";
                accionesFinales.style.display = "block";
                alert(respuesta.mensaje);
            } else {
                alert("Error: " + (respuesta ? respuesta.mensaje : "No se pudo procesar la solicitud."));
            }
        });
    });

    // Exportación Opcional de PDF
    btnExportarPDF.addEventListener("click", () => {
        if (!datosMantenimientoUltimo) return;

        eel.exportar_pdf_reporte(datosMantenimientoUltimo)((respuesta) => {
            if (respuesta && respuesta.exito) {
                alert(`📄 PDF generado con éxito en:\n${respuesta.ruta_pdf}`);
            } else {
                alert("No se pudo generar el documento PDF.");
            }
        });
    });

    // Guardar Histórico de forma limpia y retornar al Dashboard
    if (btnGuardar) {
        btnGuardar.addEventListener("click", (e) => {
            e.preventDefault();
            alert("Mantenimiento registrado en el historial del sistema.");
            regresarDashboard();
        });
    }
});