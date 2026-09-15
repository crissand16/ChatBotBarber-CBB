from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.agenda import Agenda
from app.models.detalle import Detalle
from app.models.servicio_disponibilidad import ServicioDisponibilidad
from app.models.disponibilidad import Disponibilidad
from app.models.usuario import Usuario
from app.schema.agenda_schema import AgendaCreate


# =========================================================
# CARGA EAGER USADA EN LOS LISTADOS DE AGENDAS
# =========================================================
# Evita el problema N+1: en una sola tanda de queries trae
# cliente, detalles -> servicio_disponibilidad -> servicio
# y detalles -> servicio_disponibilidad -> disponibilidad -> especialista.

_EAGER_AGENDA = (
    joinedload(Agenda.cliente),
    joinedload(Agenda.detalles)
        .joinedload(Detalle.servicio_disponibilidad)
        .joinedload(ServicioDisponibilidad.servicio),
    joinedload(Agenda.detalles)
        .joinedload(Detalle.servicio_disponibilidad)
        .joinedload(ServicioDisponibilidad.disponibilidad)
        .joinedload(Disponibilidad.especialista),
)


# =========================================================
# HELPER: SERIALIZAR UNA AGENDA (con cliente/especialista/servicios)
# =========================================================

# como son lo datos en ORM y como los va a ver el cliente de la API

def _serializar_agenda(agenda: Agenda) -> dict:
    servicios = []
    disponibilidad = None

    for detalle in agenda.detalles:
        sd = detalle.servicio_disponibilidad
        if not sd:
            continue

        if sd.servicio:
            servicios.append({
                "id_servicio": sd.servicio.id_servicios,
                "nombre": sd.servicio.nombre_servicio,
                "precio": float(sd.servicio.precio_servicio)
            })

        if disponibilidad is None:
            disponibilidad = sd.disponibilidad

    especialista = disponibilidad.especialista if disponibilidad else None
    cliente = agenda.cliente

    return {
        "id_agenda": agenda.id_agenda,
        "estado_agenda": agenda.estado_agenda,
        "precio_total": float(agenda.precio_total) if agenda.precio_total is not None else 0.0,
        "fecha_creacion_agenda": (
            agenda.fecha_creacion_agenda.isoformat()
            if agenda.fecha_creacion_agenda else None
        ),
        "fecha_agenda": (
            str(disponibilidad.fecha_disponibilidad) if disponibilidad else None
        ),
        "hora_agenda": (
            str(disponibilidad.hora_inicio_disponibilidad) if disponibilidad else None
        ),
        "cliente": {
            "id": cliente.id_usuario,
            "nombre": f"{cliente.nombres_usuario} {cliente.apellidos_usuario}".strip()
        } if cliente else None,
        "especialista": {
            "id": especialista.id_usuario,
            "nombre": f"{especialista.nombres_usuario} {especialista.apellidos_usuario}".strip()
        } if especialista else None,
        "servicios": servicios
    }

# =========================================================
# HELPER: LIBERAR LA DISPONIBILIDAD ASOCIADA A UNA AGENDA
# =========================================================
# Se usa al cancelar una agenda: recorre sus detalles y marca
# como "disponible" cada bloque de horario que había quedado
# "ocupado" al agendar.

def _liberar_disponibilidades(agenda: Agenda):
    for detalle in agenda.detalles:
        sd = detalle.servicio_disponibilidad
        if sd and sd.disponibilidad:
            sd.disponibilidad.estado_disponibilidad = "disponible"



# =========================================================
# CREAR UNA AGENDA
# =========================================================

def crear_agenda(db: Session, datos: AgendaCreate):
    try:
        # =====================================================
        # 1. VERIFICAR CLIENTE
        # =====================================================

        usuario = (
            db.query(Usuario)
            .filter(Usuario.id_usuario == datos.id_cliente)
            .first()
        )

        if not usuario:
            raise ValueError("El usuario no existe")

        # =====================================================
        # 2. VERIFICAR DISPONIBILIDAD (con bloqueo de fila)
        # =====================================================

        servicio_disponibilidad = (
            db.query(ServicioDisponibilidad)
            .options(
                joinedload(ServicioDisponibilidad.disponibilidad),
                joinedload(ServicioDisponibilidad.servicio)
            )
            .filter(
                ServicioDisponibilidad.id_servicio_disponibilidad
                == datos.id_servicio_disponibilidad
            )
            .with_for_update()
            .first()
        )

        if not servicio_disponibilidad:
            raise ValueError(
                "No se encontró el servicio o disponibilidad especificada"
            )

        disponibilidad = servicio_disponibilidad.disponibilidad
        servicio = servicio_disponibilidad.servicio

        if not disponibilidad or not servicio:
            raise ValueError(
                "No se encontró el servicio o disponibilidad especificada"
            )

        if disponibilidad.estado_disponibilidad != "disponible":
            raise ValueError("El horario seleccionado ya no está disponible")

        # =========================================================
        # 3. CREAR AGENDA CON EL PRECIO CALCULADO AUTOMÁTICAMENTE
        # =========================================================

        estado_agenda_val = getattr(datos, "estado_agenda", None) or "pendiente"

        agenda = Agenda(
            id_cliente=datos.id_cliente,
            precio_total=float(servicio.precio_servicio),
            estado_agenda=estado_agenda_val,
            fecha_creacion_agenda=datetime.now()
        )

        db.add(agenda)
        db.flush()  # genera agenda.id_agenda sin hacer commit todavía

        # =====================================================
        # 4. REGISTRAR EL DETALLE DE LA AGENDA
        # =====================================================

        detalle = Detalle(
            id_agenda=agenda.id_agenda,
            id_servicio_disponibilidad=datos.id_servicio_disponibilidad
        )
        db.add(detalle)

        # =====================================================
        # 5. ACTUALIZAR DISPONIBILIDAD A 'OCUPADO'
        # =====================================================

        disponibilidad.estado_disponibilidad = "ocupado"

        db.commit()
        db.refresh(agenda)
        return agenda

    except Exception as e:
        db.rollback()
        raise e


# =========================================================
# LISTAR CITAS POR ESPECIALISTA
# =========================================================

def obtener_citas_especialista(db: Session, id_especialista: str):
    agendas = (
        db.query(Agenda)
        .join(Detalle, Detalle.id_agenda == Agenda.id_agenda)
        .join(
            ServicioDisponibilidad,
            ServicioDisponibilidad.id_servicio_disponibilidad
            == Detalle.id_servicio_disponibilidad
        )
        .join(
            Disponibilidad,
            Disponibilidad.id_disponibilidad == ServicioDisponibilidad.id_disponibilidad
        )
        .filter(Disponibilidad.id_especialista == id_especialista)
        .options(*_EAGER_AGENDA)
        .order_by(
            Disponibilidad.fecha_disponibilidad.desc(),
            Disponibilidad.hora_inicio_disponibilidad.desc()
        )
        .distinct()
        .all() # valores únicos
    )

    return [_serializar_agenda(a) for a in agendas]


# =========================================================
# LISTAR AGENDAS POR CLIENTE
# =========================================================

def obtener_agendas_por_cliente(db: Session, id_cliente: str):
    agendas = (
        db.query(Agenda)
        .filter(Agenda.id_cliente == id_cliente)
        .options(*_EAGER_AGENDA)
        .order_by(Agenda.fecha_creacion_agenda.desc())
        .all()
    )

    return [_serializar_agenda(a) for a in agendas]


# =========================================================
# LISTAR AGENDAS POR FECHA
# =========================================================

def obtener_agendas_por_fecha(db: Session, fecha: str):
    agendas = (
        db.query(Agenda)
        .join(Detalle, Detalle.id_agenda == Agenda.id_agenda)
        .join(
            ServicioDisponibilidad,
            ServicioDisponibilidad.id_servicio_disponibilidad
            == Detalle.id_servicio_disponibilidad
        )
        .join(
            Disponibilidad,
            Disponibilidad.id_disponibilidad == ServicioDisponibilidad.id_disponibilidad
        )
        .filter(Disponibilidad.fecha_disponibilidad == fecha)
        .options(*_EAGER_AGENDA)
        .order_by(Disponibilidad.hora_inicio_disponibilidad.asc())
        .distinct()
        .all()
    )

    return [_serializar_agenda(a) for a in agendas]


# =========================================================
# LISTAR TODAS LAS AGENDAS
# =========================================================

def obtener_agendas(db: Session):
    agendas = (
        db.query(Agenda)
        .options(*_EAGER_AGENDA)
        .order_by(Agenda.fecha_creacion_agenda.desc())
        .all()
    )

    return [_serializar_agenda(a) for a in agendas]



# =========================================================
# ACTUALIZAR SOLO EL ESTADO DE UNA AGENDA
# =========================================================
# Usada por PATCH /agendas/{id_agenda}/estado.
# Si el nuevo estado es "cancelada", libera la disponibilidad
# asociada.

def actualizar_estado_agenda(db: Session, id_agenda: int, nuevo_estado: str) -> Agenda:
    agenda = (
        db.query(Agenda)
        .options(*_EAGER_AGENDA)
        .filter(Agenda.id_agenda == id_agenda)
        .first()
    )

    if not agenda:
        raise ValueError(f"La agenda con ID {id_agenda} no fue encontrada.")

    nuevo_estado = nuevo_estado.lower().strip()
    agenda.estado_agenda = nuevo_estado

    if nuevo_estado == "cancelada":
        _liberar_disponibilidades(agenda)

    db.commit()
    db.refresh(agenda)
    return agenda



# =========================================================
# CANCELAR (anular) UNA AGENDA
# =========================================================
# No se hace un DELETE físico de la fila: se marca la agenda
# como "cancelada" y se libera su disponibilidad asociada,
# para conservar el historial y no romper la FK de Detalle/Factura.

def cancelar_agenda(db: Session, id_agenda: int) -> bool:
    agenda = (
        db.query(Agenda)
        .options(*_EAGER_AGENDA)
        .filter(Agenda.id_agenda == id_agenda)
        .first()
    )

    if not agenda:
        return False

    agenda.estado_agenda = "cancelada"
    _liberar_disponibilidades(agenda)

    db.commit()
    return True
