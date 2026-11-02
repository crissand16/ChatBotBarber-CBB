from datetime import date
from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.reporte_controller import (
    ESTADOS_AGENDA,
    ESTADOS_FACTURA,
    reporte_agendas,
    reporte_facturas,
)
from app.utils.reportes import generar_excel, generar_pdf
from app.utils.response import response_error

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

MIME_EXCEL = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
MIME_PDF = "application/pdf"


def _archivo(contenido: bytes, mime: str, nombre: str) -> StreamingResponse:
    return StreamingResponse(
        BytesIO(contenido),
        media_type=mime,
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )


def _validar_rango(fecha_inicio: date, fecha_fin: date):
    if fecha_inicio > fecha_fin:
        return response_error(
            mensaje="La fecha inicial no puede ser mayor que la fecha final",
            error="INVALID_DATE_RANGE",
            code=400
        )
    return None


def _validar_estado(estado: Optional[str], permitidos: tuple):
    if estado and estado not in permitidos:
        return response_error(
            mensaje=f"Estado no permitido. Use uno de: {', '.join(permitidos)}",
            error="INVALID_STATE",
            code=400
        )
    return None


# =========================================================
# CITAS (AGENDAS)
# =========================================================

def _reporte_agendas_archivo(
    formato: str,
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str],
    id_especialista: Optional[str],
    db: Session,
):
    try:
        error = _validar_rango(fecha_inicio, fecha_fin) or _validar_estado(estado, ESTADOS_AGENDA)
        if error:
            return error

        reporte = reporte_agendas(db, fecha_inicio, fecha_fin, estado, id_especialista)
        nombre = f"reporte_citas_{fecha_inicio}_{fecha_fin}"

        if formato == "excel":
            return _archivo(generar_excel(reporte), MIME_EXCEL, f"{nombre}.xlsx")
        return _archivo(generar_pdf(reporte), MIME_PDF, f"{nombre}.pdf")

    except Exception as error:
        return response_error(
            mensaje="Error al generar el reporte de citas",
            error=str(error),
            code=500
        )


@router.get("/agendas/excel")
def agendas_excel(
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str] = None,
    id_especialista: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return _reporte_agendas_archivo("excel", fecha_inicio, fecha_fin, estado, id_especialista, db)


@router.get("/agendas/pdf")
def agendas_pdf(
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str] = None,
    id_especialista: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return _reporte_agendas_archivo("pdf", fecha_inicio, fecha_fin, estado, id_especialista, db)


# =========================================================
# FACTURACIÓN
# =========================================================

def _reporte_facturas_archivo(
    formato: str,
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str],
    db: Session,
):
    try:
        error = _validar_rango(fecha_inicio, fecha_fin) or _validar_estado(estado, ESTADOS_FACTURA)
        if error:
            return error

        reporte = reporte_facturas(db, fecha_inicio, fecha_fin, estado)
        nombre = f"reporte_facturacion_{fecha_inicio}_{fecha_fin}"

        if formato == "excel":
            return _archivo(generar_excel(reporte), MIME_EXCEL, f"{nombre}.xlsx")
        return _archivo(generar_pdf(reporte), MIME_PDF, f"{nombre}.pdf")

    except Exception as error:
        return response_error(
            mensaje="Error al generar el reporte de facturación",
            error=str(error),
            code=500
        )


@router.get("/facturas/excel")
def facturas_excel(
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return _reporte_facturas_archivo("excel", fecha_inicio, fecha_fin, estado, db)


@router.get("/facturas/pdf")
def facturas_pdf(
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return _reporte_facturas_archivo("pdf", fecha_inicio, fecha_fin, estado, db)
