import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


if not DATABASE_URL:
    raise ValueError(
        "Falta la variable DATABASE_URL"
    )


# =========================================================
# CORREO (buzón PQR)
# =========================================================
# Las PQR (peticiones, quejas y reclamos) se envían por SMTP a la cuenta
# de Gmail del administrador. Para Gmail NO se usa la contraseña normal de
# la cuenta sino una "contraseña de aplicación" (ver README / .env).

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")

SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

SMTP_USER = os.getenv("SMTP_USER", "adminchatbotbarber@gmail.com")

# Gmail muestra la contraseña de aplicación con espacios (abcd efgh ...);
# se quitan para que funcione pegada tal cual.
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").replace(" ", "")

SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

# Correo que recibe (y responde) todas las PQR.
PQR_DESTINATARIO = os.getenv("PQR_DESTINATARIO", "adminchatbotbarber@gmail.com")
