// Lógica de interfaz para Gestión Documental con Eel (Control de Versiones, Descargas y Selección Múltiple)

document.addEventListener("DOMContentLoaded", () => {
    cargarListaDocumentos();

    const docForm = document.getElementById("documento-form");
    if (docForm) {
        docForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const nombreDoc = document.getElementById("doc_nombre").value;
            const categoria = document.getElementById("doc_categoria").value;
            const archivoInput = document.getElementById("doc_archivo");

            if (!archivoInput || !archivoInput.files[0]) {
                alert("Por favor seleccione un archivo digital de su PC.");
                return;
            }

            const nombreArchivo = archivoInput.files[0].name;
            const usuarioActual = sessionStorage.getItem("usuario") || sessionStorage.getItem("rol") || "Administrador";

            eel.registrar_documento(nombreDoc, categoria, nombreArchivo, usuarioActual)((response) => {
                if (response && response.exito) {
                    alert(`¡Éxito! ${response.mensaje}`);
                    docForm.reset();
                    cargarListaDocumentos();
                } else {
                    alert("Error al registrar documento: " + (response ? response.mensaje : "Desconocido"));
                }
            });
        });
    }

    // Seleccionar / Deseleccionar todos los checkboxes
    const selectAllCheckbox = document.getElementById("select-all");
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener("change", (e) => {
            const checkboxes = document.querySelectorAll(".doc-checkbox");
            checkboxes.forEach(cb => cb.checked = e.target.checked);
        });
    }

    // Botón Descargar Seleccionados
    const btnDescargarLote = document.getElementById("btn-descargar-lote");
    if (btnDescargarLote) {
        btnDescargarLote.addEventListener("click", () => {
            const seleccionados = document.querySelectorAll(".doc-checkbox:checked");
            if (seleccionados.length === 0) {
                alert("Por favor seleccione al menos un documento para descargar.");
                return;
            }

            seleccionados.forEach(cb => {
                const nombreArchivo = cb.getAttribute("data-archivo");
                eel.descargar_archivo_local(nombreArchivo)((res) => {
                    if (res && res.exito) {
                        console.log(`Archivo descargado en: ${res.ruta}`);
                    }
                });
            });
            alert(`¡Se han exportado ${seleccionados.length} archivo(s) a la carpeta Descargas de su dispositivo con éxito!`);
        });
    }

    // Botón Eliminar Seleccionados
    const btnEliminarLote = document.getElementById("btn-eliminar-lote");
    if (btnEliminarLote) {
        btnEliminarLote.addEventListener("click", () => {
            const seleccionados = document.querySelectorAll(".doc-checkbox:checked");
            if (seleccionados.length === 0) {
                alert("Por favor seleccione al menos un registro para eliminar.");
                return;
            }

            if (!confirm(`¿Está seguro de eliminar los ${seleccionados.length} registros seleccionados del sistema?`)) {
                return;
            }

            const idsAEliminar = Array.from(seleccionados).map(cb => parseInt(cb.value));

            eel.eliminar_documentos(idsAEliminar)((res) => {
                if (res && res.exito) {
                    alert(res.mensaje);
                    cargarListaDocumentos();
                    if (selectAllCheckbox) selectAllCheckbox.checked = false;
                } else {
                    alert("Error al eliminar: " + (res ? res.mensaje : "Desconocido"));
                }
            });
        });
    }
});

// Función para consultar y pintar los documentos en la tabla con checkboxes
function cargarListaDocumentos() {
    const tbody = document.getElementById("tabla-documentos-body");
    if (!tbody) return;

    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #7f8c8d;">Cargando registros institucionales...</td></tr>`;

    eel.listar_documentos()((res) => {
        tbody.innerHTML = "";

        if (!res || !res.exito || !res.documentos || res.documentos.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #7f8c8d;">No hay documentos registrados en el sistema.</td></tr>`;
            return;
        }

        res.documentos.forEach((doc) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td style="text-align: center;"><input type="checkbox" class="doc-checkbox" value="${doc.id}" data-archivo="${doc.archivo}"></td>
                <td>${doc.id}</td>
                <td><strong>${doc.nombre}</strong> <span style="background: #e2e8f0; color: #2d3748; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">${doc.version || 'V1.0'}</span></td>
                <td>${doc.categoria}</td>
                <td>
                    <a href="#" onclick="eel.descargar_archivo_local('${doc.archivo}')(() => alert('Archivo descargado en la carpeta Descargas de su PC.')); return false;" style="color: #2980b9; text-decoration: none; font-weight: 600;">
                        📎 ${doc.archivo || 'N/A'}
                    </a>
                </td>
                <td>${doc.fecha_registro}</td>
                <td><span style="color: #27ae60; font-weight: 600;">${doc.registrado_por}</span></td>
            `;
            tbody.appendChild(tr);
        });
    });
}