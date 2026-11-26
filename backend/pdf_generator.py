import os
from datetime import datetime
from db import obtener_conexion  # <-- Conexión a la base de datos ueam_dh (puerto 3307)

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
    Genera un archivo PDF (o TXT de respaldo) con el reporte técnico del mantenimiento/diagnóstico
    directamente en la carpeta Descargas del usuario y registra la auditoría en la base de datos.
    """
    if not isinstance(datos_diag, dict):
        datos_diag = {}

    # Apuntar directamente a la carpeta Descargas del usuario de forma multiplataforma
    output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    codigo = datos_diag.get('codigo_equipo', 'EQ')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if REPORTLAB_AVAILABLE:
        filename = f"Reporte_Mantenimiento_{codigo}_{timestamp}.pdf"
    else:
        filename = f"Reporte_Mantenimiento_{codigo}_{timestamp}.txt"

    filepath = os.path.join(output_dir, filename)

    # Extraer valores para la base de datos
    fecha_reporte = datos_diag.get("fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sistema_op = datos_diag.get("sistema_operativo", "N/A")
    tipo_mant = datos_diag.get("tipo_mantenimiento", "Preventivo")
    estado_gen = datos_diag.get("estado_general", "Operativo")
    responsable = datos_diag.get("responsable", "Estudiante")
    observaciones = datos_diag.get("observaciones_tecnicas", "Sin detalles adicionales")

    # --- Integración SQL: Guardar registro del reporte en la BD ---
    conexion = obtener_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO reportes_diagnostico 
                    (codigo_equipo, fecha, sistema_operativo, tipo_mantenimiento, estado_general, responsable, observaciones_tecnicas, archivo_generado) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    str(codigo),
                    str(fecha_reporte),
                    str(sistema_op),
                    str(tipo_mant),
                    str(estado_gen),
                    str(responsable),
                    str(observaciones),
                    str(filename)
                ))
                conexion.commit()
        except Exception as sql_err:
            print(f"Aviso de base de datos en PDF (no afecta la exportación): {sql_err}")
        finally:
            conexion.close()
    # -------------------------------------------------------------

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
                ["Fecha / Hora:", fecha_reporte],
                ["Código de Equipo:", codigo],
                ["Sistema Operativo:", sistema_op],
                ["Tipo de Mantenimiento:", tipo_mant],
                ["Estado General:", estado_gen],
                ["Técnico / Responsable:", responsable],
                ["Observaciones:", observaciones]
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

            # IMPORTANTE: Se incluye tanto 'ruta' como 'ruta_pdf' para compatibilidad total con el frontend
            return {
                "exito": True,
                "ruta": filepath,
                "ruta_pdf": filepath,
                "nombre_archivo": filename,
                "mensaje": "Reporte exportado con éxito."
            }

        except Exception as e:
            return {"exito": False, "mensaje": f"Error compilando PDF: {str(e)}"}
    else:
        # Fallback en texto si reportlab no está instalado
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("=== REPORTE DE MANTENIMIENTO UEAM ===\n\n")
                for clave, valor in datos_diag.items():
                    f.write(f"{clave.replace('_', ' ').title()}: {valor}\n")

            return {
                "exito": True,
                "ruta": filepath,
                "ruta_pdf": filepath,
                "nombre_archivo": filename,
                "mensaje": "Reporte exportado con éxito.",
                "nota": "ReportLab no instalado; se generó archivo en TXT en Descargas."
            }
        except Exception as e:
            return {"exito": False, "mensaje": f"Error en respaldo TXT: {str(e)}"}