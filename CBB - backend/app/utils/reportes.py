"""Generadores de archivos de reporte (Excel y PDF).

Son funciones puras: reciben un diccionario con el contenido del reporte
y devuelven los bytes del archivo. No conocen FastAPI ni SQLAlchemy.

Forma esperada del reporte:
{
    "titulo": "Reporte de citas",
    "filtros": [("Desde", "2026-10-01"), ("Hasta", "2026-10-31")],
    "columnas": ["ID", "Fecha", "Total"],
    "filas": [[1, "2026-10-05", 25000.0], ...],
    "columnas_moneda": [2],          # índices de columnas con valores en pesos
    "pesos_columnas": [1, 2, 1],     # opcional: anchos relativos en el PDF
    "resumen": [("Total de citas", 12), ("Valor total", 300000.0)],
}
"""
from datetime import datetime
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

COLOR_ENCABEZADO = "1F3A5F"
COLOR_ZEBRA = "F2F5F9"
FORMATO_MONEDA_EXCEL = '"$"#,##0'


def _moneda(valor) -> str:
    """12345.5 -> '$12.346' (separador de miles con punto, sin decimales)."""
    return "$" + f"{float(valor):,.0f}".replace(",", ".")


def _ahora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# =========================================================
# EXCEL
# =========================================================

def generar_excel(reporte: dict) -> bytes:
    columnas = reporte["columnas"]
    filas = reporte["filas"]
    monedas = set(reporte.get("columnas_moneda", []))
    total_cols = len(columnas)

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    # Título
    ws.cell(row=1, column=1, value=reporte["titulo"]).font = Font(bold=True, size=14)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=total_cols)
    ws.cell(row=2, column=1, value=f"Generado el {_ahora()}").font = Font(italic=True, color="666666")

    # Filtros aplicados
    fila = 3
    for nombre, valor in reporte.get("filtros", []):
        ws.cell(row=fila, column=1, value=f"{nombre}:").font = Font(bold=True)
        ws.cell(row=fila, column=2, value=str(valor))
        fila += 1

    # Encabezado de la tabla
    fila_encabezado = fila + 1
    borde = Side(style="thin", color="CCCCCC")
    for c, nombre in enumerate(columnas, start=1):
        celda = ws.cell(row=fila_encabezado, column=c, value=nombre)
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill("solid", fgColor=COLOR_ENCABEZADO)
        celda.alignment = Alignment(horizontal="center", vertical="center")
        celda.border = Border(top=borde, bottom=borde, left=borde, right=borde)

    # Filas de datos
    for i, datos in enumerate(filas, start=1):
        for c, valor in enumerate(datos, start=1):
            celda = ws.cell(row=fila_encabezado + i, column=c, value=valor)
            celda.border = Border(top=borde, bottom=borde, left=borde, right=borde)
            celda.alignment = Alignment(vertical="top", wrap_text=True)
            if (c - 1) in monedas:
                celda.number_format = FORMATO_MONEDA_EXCEL
            if i % 2 == 0:
                celda.fill = PatternFill("solid", fgColor=COLOR_ZEBRA)

    ultima_fila = fila_encabezado + len(filas)

    # Resumen
    fila_resumen = ultima_fila + 2
    for nombre, valor in reporte.get("resumen", []):
        ws.cell(row=fila_resumen, column=1, value=nombre).font = Font(bold=True)
        celda = ws.cell(row=fila_resumen, column=2, value=valor)
        if isinstance(valor, float):
            celda.number_format = FORMATO_MONEDA_EXCEL
        fila_resumen += 1

    # Anchos de columna según el contenido (con tope)
    for c in range(1, total_cols + 1):
        mayor = max(
            (len(str(ws.cell(row=r, column=c).value or "")) for r in range(fila_encabezado, ultima_fila + 1)),
            default=10,
        )
        ws.column_dimensions[get_column_letter(c)].width = min(max(mayor + 3, 12), 45)

    ws.freeze_panes = ws.cell(row=fila_encabezado + 1, column=1)
    if filas:
        ws.auto_filter.ref = f"A{fila_encabezado}:{get_column_letter(total_cols)}{ultima_fila}"

    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


# =========================================================
# PDF
# =========================================================

def generar_pdf(reporte: dict) -> bytes:
    columnas = reporte["columnas"]
    filas = reporte["filas"]
    monedas = set(reporte.get("columnas_moneda", []))

    estilos = getSampleStyleSheet()
    estilo_celda = ParagraphStyle("celda", parent=estilos["BodyText"], fontSize=8, leading=10)
    estilo_filtros = ParagraphStyle("filtros", parent=estilos["BodyText"], fontSize=9, textColor=colors.HexColor("#444444"))

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title=reporte["titulo"],
    )

    contenido = [Paragraph(reporte["titulo"], estilos["Title"])]
    filtros = "  |  ".join(f"<b>{n}:</b> {v}" for n, v in reporte.get("filtros", []))
    contenido.append(Paragraph(f"{filtros}  |  <b>Generado:</b> {_ahora()}", estilo_filtros))
    contenido.append(Spacer(1, 0.4 * cm))

    # Tabla principal. Las celdas de texto van en Paragraph para que ajusten línea.
    datos = [columnas]
    for fila in filas:
        celdas = []
        for c, valor in enumerate(fila):
            texto = _moneda(valor) if c in monedas else str(valor)
            celdas.append(Paragraph(texto, estilo_celda))
        datos.append(celdas)
    if not filas:
        datos.append([Paragraph("Sin registros para los filtros indicados", estilo_celda)] + [""] * (len(columnas) - 1))

    # Anchos relativos opcionales ("pesos_columnas"); si no vienen, se reparten por igual.
    pesos = reporte.get("pesos_columnas")
    ancho_util = landscape(A4)[0] - 3 * cm
    anchos = [ancho_util * p / sum(pesos) for p in pesos] if pesos else None
    tabla = Table(datos, repeatRows=1, colWidths=anchos)
    estilo_tabla = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#" + COLOR_ENCABEZADO)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#" + COLOR_ZEBRA)]),
    ]
    if not filas:
        estilo_tabla.append(("SPAN", (0, 1), (-1, 1)))
    tabla.setStyle(TableStyle(estilo_tabla))
    contenido.append(tabla)

    # Resumen
    resumen = reporte.get("resumen", [])
    if resumen:
        contenido.append(Spacer(1, 0.6 * cm))
        contenido.append(Paragraph("Resumen", estilos["Heading3"]))
        filas_resumen = [
            [nombre, _moneda(valor) if isinstance(valor, float) else str(valor)]
            for nombre, valor in resumen
        ]
        tabla_resumen = Table(filas_resumen, colWidths=[7 * cm, 4 * cm], hAlign="LEFT")
        tabla_resumen.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
        ]))
        contenido.append(tabla_resumen)

    def pie_de_pagina(canvas, documento):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawRightString(landscape(A4)[0] - 1.5 * cm, 0.8 * cm, f"Página {documento.page}")
        canvas.restoreState()

    doc.build(contenido, onFirstPage=pie_de_pagina, onLaterPages=pie_de_pagina)
    return buffer.getvalue()
