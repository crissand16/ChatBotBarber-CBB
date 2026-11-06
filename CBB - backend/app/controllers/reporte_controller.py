from datetime import date, datetime, time, timedelta
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.controllers.agenda_controller import _EAGER_AGENDA, _serializar_agenda
from app.models.agenda import Agenda
from app.models.detalle import Detalle
from app.models.disponibilidad import Disponibilidad
from app.models.factura import Factura
from app.models.servicio_disponibilidad import ServicioDisponibilidad
from app.models.usuario import Usuario

ESTADOS_AGENDA = ("pendiente", "aceptada", "rechazada", "completada", "cancelada")
ESTADOS_FACTURA = ("pendiente", "pagada")


def _nombre(usuario: Optional[Usuario]) -> str:
    if not usuario:
        return "-"
    return f"{usuario.nombres_usuario} {usuario.apellidos_usuario}".strip()


# =========================================================
# REPORTE DE AGENDAS (CITAS)
# =========================================================
# El rango de fechas se aplica sobre la fecha de la CITA
# (disponibilidad), no sobre la fecha en que se creó la agenda.

def reporte_agendas(
    db: Session,
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str] = None,
    id_especialista: Optional[str] = None,
) -> dict:
    consulta = (
        db.query(Agenda)
        .join(Detalle, Detalle.id_agenda == Agenda.id_agenda)
        .join(
            ServicioDisponibilidad,
            ServicioDisponibilidad.id_servicio_disponibilidad
            == Detalle.id_servicio_disponibilidad,
        )
        .join(
            Disponibilidad,
            Disponibilidad.id_disponibilidad == ServicioDisponibilidad.id_disponibilidad,
        )
        .filter(Disponibilidad.fecha_disponibilidad.between(fecha_inicio, fecha_fin))
        .options(*_EAGER_AGENDA)
    )

    if estado:
        consulta = consulta.filter(Agenda.estado_agenda == estado)
    if id_especialista:
        consulta = consulta.filter(Disponibilidad.id_especialista == id_especialista)

    registros = consulta.order_by(
        Disponibilidad.fecha_disponibilidad,
        Disponibilidad.hora_inicio_disponibilidad,
    ).all()

    # El JOIN con detalle repite la agenda una vez por servicio: se deduplica.
    vistos, agendas = set(), []
    for agenda in registros:
        if agenda.id_agenda not in vistos:
            vistos.add(agenda.id_agenda)
            agendas.append(_serializar_agenda(agenda))

    filas = [
        [
            a["id_agenda"],
            a["fecha_agenda"] or "-",
            (a["hora_agenda"] or "-")[:5],
            a["cliente"]["nombre"] if a["cliente"] else "-",
            a["especialista"]["nombre"] if a["especialista"] else "-",
            ", ".join(s["nombre"] for s in a["servicios"]) or "-",
            a["estado_agenda"],
            a["precio_total"],
        ]
        for a in agendas
    ]

    por_estado = {}
    for a in agendas:
        por_estado[a["estado_agenda"]] = por_estado.get(a["estado_agenda"], 0) + 1
    valor_completadas = sum(
        a["precio_total"] for a in agendas if a["estado_agenda"] == "completada"
    )

    resumen = [("Total de citas", len(agendas))]
    resumen += [(f"Citas {e}s", por_estado[e]) for e in ESTADOS_AGENDA if e in por_estado]
    resumen.append(("Valor de citas completadas", float(valor_completadas)))

    return {
        "titulo": "Reporte de citas",
        "filtros": [
            ("Desde", fecha_inicio.isoformat()),
            ("Hasta", fecha_fin.isoformat()),
            ("Estado", estado or "todos"),
            ("Especialista", id_especialista or "todos"),
        ],
        "columnas": ["ID", "Fecha", "Hora", "Cliente", "Especialista", "Servicios", "Estado", "Total"],
        "filas": filas,
        "columnas_moneda": [7],
        "pesos_columnas": [0.6, 1.2, 0.9, 2.2, 2.2, 3.4, 1.4, 1.4],
        "resumen": resumen,
    }


# =========================================================
# REPORTE DE FACTURACIÓN
# =========================================================

def reporte_facturas(
    db: Session,
    fecha_inicio: date,
    fecha_fin: date,
    estado: Optional[str] = None,
) -> dict:
    # fecha_factura es TIMESTAMP: el límite superior es "antes de medianoche del día siguiente"
    desde = datetime.combine(fecha_inicio, time.min)
    hasta = datetime.combine(fecha_fin + timedelta(days=1), time.min)

    consulta = (
        db.query(Factura)
        .options(joinedload(Factura.agenda).joinedload(Agenda.cliente))
        .filter(Factura.fecha_factura >= desde, Factura.fecha_factura < hasta)
    )
    if estado:
        consulta = consulta.filter(Factura.estado_factura == estado)

    facturas = consulta.order_by(Factura.fecha_factura).all()

    filas = [
        [
            f.id_factura,
            f.fecha_factura.strftime("%Y-%m-%d %H:%M"),
            f.id_agenda,
            _nombre(f.agenda.cliente if f.agenda else None),
            float(f.subtotal_factura),
            float(f.iva_factura),
            float(f.total_factura),
            f.estado_factura,
            f.metodo_pago_factura,
        ]
        for f in facturas
    ]

    total = sum(float(f.total_factura) for f in facturas)
    pagado = sum(float(f.total_factura) for f in facturas if f.estado_factura == "pagada")

    return {
        "titulo": "Reporte de facturación",
        "filtros": [
            ("Desde", fecha_inicio.isoformat()),
            ("Hasta", fecha_fin.isoformat()),
            ("Estado", estado or "todos"),
        ],
        "columnas": ["N° factura", "Fecha", "Agenda", "Cliente", "Subtotal", "IVA", "Total", "Estado", "Método de pago"],
        "filas": filas,
        "columnas_moneda": [4, 5, 6],
        "pesos_columnas": [1, 1.8, 0.9, 2.6, 1.3, 1.2, 1.3, 1.2, 1.6],
        "resumen": [
            ("Total de facturas", len(facturas)),
            ("Subtotal", float(sum(float(f.subtotal_factura) for f in facturas))),
            ("IVA", float(sum(float(f.iva_factura) for f in facturas))),
            ("Total facturado", float(total)),
            ("Total pagado", float(pagado)),
            ("Total pendiente de pago", float(total - pagado)),
        ],
    }