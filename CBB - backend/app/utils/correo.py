"""Envío de correos por SMTP (usado por el buzón PQR).

Solo usa la librería estándar de Python (smtplib / email), así que no
agrega dependencias nuevas a requirements.txt.
"""

import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from typing import Optional

from app.config import settings


class CorreoNoConfigurado(Exception):
    """Falta SMTP_USER o SMTP_PASSWORD en el .env."""


def correo_configurado() -> bool:
    return bool(settings.SMTP_USER and settings.SMTP_PASSWORD)


def construir_mensaje(
    destinatario: str,
    asunto: str,
    texto: str,
    html: Optional[str] = None,
    reply_to: Optional[str] = None,
) -> EmailMessage:
    mensaje = EmailMessage()

    mensaje["From"] = formataddr(("ChatBotBarber", settings.SMTP_USER))
    mensaje["To"] = destinatario
    # Un asunto de una sola línea evita inyección de cabeceras.
    mensaje["Subject"] = " ".join(asunto.split())

    # Con Reply-To, al pulsar "Responder" en Gmail la respuesta viaja
    # directo al correo del cliente que escribió la PQR.
    if reply_to:
        mensaje["Reply-To"] = reply_to

    mensaje.set_content(texto)

    if html:
        mensaje.add_alternative(html, subtype="html")

    return mensaje


def enviar_correo(
    destinatario: str,
    asunto: str,
    texto: str,
    html: Optional[str] = None,
    reply_to: Optional[str] = None,
) -> None:
    """Envía el correo. Lanza excepción si no se pudo enviar."""

    if not correo_configurado():
        raise CorreoNoConfigurado(
            "Falta configurar SMTP_USER y SMTP_PASSWORD en el archivo .env"
        )

    mensaje = construir_mensaje(destinatario, asunto, texto, html, reply_to)

    if settings.SMTP_PORT == 465:
        servidor = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20)
    else:
        servidor = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20)

    with servidor:
        if settings.SMTP_PORT != 465 and settings.SMTP_USE_TLS:
            servidor.starttls()

        servidor.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        servidor.send_message(mensaje)
