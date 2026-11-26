import traceback
from html import escape

from sqlalchemy.orm import Session

from app.config import settings
from app.models.pqr import Pqr
from app.models.usuario import Usuario
from app.utils.correo import enviar_correo
from app.utils.errores import NoEncontrado

ETIQUETA_TIPO = {
    "peticion": "Petición",
    "queja": "Queja",
    "reclamo": "Reclamo",
}


# =========================================================
# CORREOS
# =========================================================

def _correo_para_administrador(pqr: Pqr) -> None:
    tipo = ETIQUETA_TIPO.get(pqr.tipo_pqr, pqr.tipo_pqr)
    fecha = pqr.fecha_creacion_pqr.strftime("%d/%m/%Y %H:%M")

    asunto = f"[{pqr.radicado}] {tipo}: {pqr.asunto_pqr}"

    texto = (
        f"Nueva {tipo.lower()} recibida en el buzón de ChatBotBarber\n"
        f"\n"
        f"Radicado: {pqr.radicado}\n"
        f"Fecha: {fecha}\n"
        f"Tipo: {tipo}\n"
        f"Usuario: {pqr.nombre_pqr} (documento {pqr.id_usuario})\n"
        f"Correo de contacto: {pqr.correo_pqr}\n"
        f"Asunto: {pqr.asunto_pqr}\n"
        f"\n"
        f"Mensaje:\n{pqr.mensaje_pqr}\n"
        f"\n"
        f"-- Para responder, solo pulsa \"Responder\": la respuesta llegará\n"
        f"directamente a {pqr.correo_pqr}."
    )

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;color:#0a0a0a">
      <h2 style="margin:0 0 4px;color:#3452e1">Nueva {escape(tipo.lower())} · {pqr.radicado}</h2>
      <p style="margin:0 0 16px;color:#6b7280;font-size:13px">Buzón de ChatBotBarber · {fecha}</p>
      <table style="border-collapse:collapse;width:100%;font-size:14px">
        <tr><td style="padding:6px 0;color:#6b7280;width:140px">Tipo</td><td><b>{escape(tipo)}
        </b></td></tr>
        <tr><td style="padding:6px 0;color:#6b7280">Usuario</td><td>{escape(pqr.nombre_pqr)}
        (doc. {escape(pqr.id_usuario)})
        </td></tr>
        <tr><td style="padding:6px 0;color:#6b7280">Correo</td><td>{escape(pqr.correo_pqr)}
        </td></tr>
        <tr><td style="padding:6px 0;color:#6b7280">Asunto</td><td>{escape(pqr.asunto_pqr)}
        </td></tr>
      </table>
      <div style="margin-top:16px;padding:14px;background:#f4f6f8;border-radius:8px;
      white-space:pre-wrap;font-size:14px">{escape(pqr.mensaje_pqr)}</div>
      <p style="margin-top:16px;font-size:12px;color:#6b7280">
        Pulsa <b>Responder</b> para contestar: la respuesta llegará directamente
        a {escape(pqr.correo_pqr)}.
      </p>
    </div>
    """

    # reply_to = correo del cliente -> el admin responde desde Gmail
    enviar_correo(
        destinatario=settings.PQR_DESTINATARIO,
        asunto=asunto,
        texto=texto,
        html=html,
        reply_to=pqr.correo_pqr,
    )


def _correo_confirmacion_cliente(pqr: Pqr) -> None:
    tipo = ETIQUETA_TIPO.get(pqr.tipo_pqr, pqr.tipo_pqr)

    texto = (
        f"Hola {pqr.nombre_pqr},\n\n"
        f"Recibimos tu {tipo.lower()} con el radicado {pqr.radicado}.\n"
        f"Asunto: {pqr.asunto_pqr}\n\n"
        f"Nuestro equipo la revisará y te responderá a este correo.\n\n"
        f"Equipo ChatBotBarber"
    )

    enviar_correo(
        destinatario=pqr.correo_pqr,
        asunto=f"Recibimos tu {tipo.lower()} ({pqr.radicado})",
        texto=texto,
        reply_to=settings.PQR_DESTINATARIO,
    )


def _notificar(pqr: Pqr) -> bool:
    """Envía los correos. Devuelve True si el del administrador salió bien.

    Nunca lanza excepción: la PQR ya está guardada en la base de datos y
    un fallo de correo no debe hacerla perder.
    """
    try:
        _correo_para_administrador(pqr)
    except Exception:
        print(f"[PQR] No se pudo notificar {pqr.radicado} por correo:")
        traceback.print_exc()
        return False

    # Confirmación al cliente: es opcional, si falla no cambia el resultado
    try:
        _correo_confirmacion_cliente(pqr)
    except Exception:
        print(f"[PQR] No se pudo enviar la confirmación al cliente de {pqr.radicado}:")
        traceback.print_exc()

    return True


# =========================================================
# CREAR PQR
# =========================================================

def crear_pqr(db: Session, datos: dict) -> Pqr:
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id_usuario == datos["id_usuario"])
        .first()
    )

    if not usuario:
        raise NoEncontrado("El usuario no existe")

    nueva = Pqr(
        id_usuario=datos["id_usuario"],
        nombre_pqr=datos["nombre"],
        correo_pqr=datos["correo"],
        tipo_pqr=datos["tipo"],
        asunto_pqr=" ".join(datos["asunto"].split()),
        mensaje_pqr=datos["mensaje"],
    )

    # 1. Primero se guarda (queda radicada aunque falle el correo)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # 2. Luego se notifica por correo y se deja constancia del resultado
    nueva.correo_enviado_pqr = _notificar(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva
