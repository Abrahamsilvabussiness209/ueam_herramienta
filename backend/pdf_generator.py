# Módulo generador de pdf

import os
from datetime import datetime

# Intentar importar reportlab; si no está instalado, se utiliza un método alternativo seguro.
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generar_pdf_diagnostico(datos_diag: dict) -> dict:
    """
    Genera un archivo PDF con el reporte técnico del mantenimiento/diagnóstico.
    """
    if not isinstance(datos_diag, dict):
        datos_diag = {}

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'storage', 'documentos')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    codigo = datos_diag.get('codigo_equipo', 'EQ')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"Reporte_Mantenimiento_{codigo}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    if REPORTLAB_AVAILABLE:
        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Encabezado
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1A365D'),
                alignment=1,
                spaceAfter=12
            )

            story.append(Paragraph("<b>HERRAMIENTA INSTITUCIONAL UEAM</b>", title_style))
            story.append(Paragraph("<b>Reporte de Mantenimiento de Software y Diagnóstico</b>", styles['Heading2']))
            story.append(Spacer(1, 12))

            # Tabla de Datos
            data = [
                ["Fecha / Hora:", datos_diag.get("fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))],
                ["Código de Equipo:", datos_diag.get("codigo_equipo", "N/A")],
                ["Sistema Operativo:", datos_diag.get("sistema_operativo", "N/A")],
                ["Tipo de Mantenimiento:", datos_diag.get("tipo_mantenimiento", "Preventivo")],
                ["Estado General:", datos_diag.get("estado_general", "Operativo")],
                ["Técnico / Responsable:", datos_diag.get("responsable", "Estudiante")],
                ["Observaciones:", datos_diag.get("observaciones_tecnicas", "Sin detalles adicionales")]
            ]

            t = Table(data, colWidths=[150, 350])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EDF2F7')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
            ]))

            story.append(t)
            doc.build(story)

            return {"exito": True, "ruta": filepath, "nombre_archivo": filename}

        except Exception as e:
            return {"exito": False, "mensaje": f"Error compilando PDF: {str(e)}"}
    else:
        # Fallback en texto si reportlab no está instalado
        txt_path = filepath.replace(".pdf", ".txt")
        try:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("=== REPORTE DE MANTENIMIENTO UEAM ===\n\n")
                for clave, valor in datos_diag.items():
                    f.write(f"{clave.replace('_', ' ').title()}: {valor}\n")

            return {
                "exito": True,
                "ruta": txt_path,
                "nombre_archivo": os.path.basename(txt_path),
                "nota": "ReportLab no instalado; se generó archivo en TXT."
            }
        except Exception as e:
            return {"exito": False, "mensaje": f"Error en respaldo TXT: {str(e)}"}
