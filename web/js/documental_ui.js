// Lógica de interfaz para Gestión Documental

// Lógica de interfaz para Gestión Documental

document.addEventListener("DOMContentLoaded", () => {
    cargarListaDocumentos();

    const docForm = document.getElementById("documento-form");
    if (docForm) {
        docForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const archivoInput = document.getElementById("doc-file");

            if (!archivoInput || !archivoInput.files[0]) {
                alert("Por favor seleccione un archivo.");
                return;
            }

            const formData = new FormData();
            formData.append("archivo", archivoInput.files[0]);

            try {
                const res = await fetch("/api/documental/subir", {
                    method: "POST",
                    body: formData
                });
                const data = await res.json();

                if (data.exito) {
                    alert("Archivo subido correctamente.");
                    cargarListaDocumentos();
                } else {
                    alert("Error al subir archivo: " + data.mensaje);
                }
            } catch (err) {
                console.error("Error documental:", err);
            }
        });
    }
});

async function cargarListaDocumentos() {
    const contenedor = document.getElementById("lista-documentos");
    if (!contenedor) return;

    try {
        const res = await fetch("/api/documental/listar");
        const docs = await res.json();

        contenedor.innerHTML = docs.map(doc => `
            <div class="doc-item">
                <span>${doc.nombre}</span>
                <a href="${doc.url}" download>Descargar</a>
            </div>
        `).join("");
    } catch (err) {
        console.error("Error listando documentos:", err);
    }
}