from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config.database import engine
from app.models import Pqr
from app.routes.agenda_routes import router as agenda_routes
from app.routes.detalle_routes import router as detalle_routes
from app.routes.disponibilidad_routes import router as disponibilidad_routes
from app.routes.factura_routes import router as factura_routes
from app.routes.pqr_routes import router as pqr_routes
from app.routes.reporte_routes import router as reporte_routes
from app.routes.servi_dispo_routes import router as servi_dispo_routes
from app.routes.servicios_routes import router as servicios_routes
from app.routes.usuario_routes import router as usuario_routes
from app.utils.scheduler import iniciar_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación
    iniciar_scheduler()
    yield
    # Código que se ejecuta al apagar la aplicación (si aplica)


try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("Conexión exitosa a la base de datos")
except Exception as error:
    print(f"Error de conexión a la base de datos: {error}")

# La tabla del buzón PQR se crea sola si todavía no existe (no toca las
# demás tablas). También está en database/12 - CREAR_PQR.sql.
try:
    Pqr.__table__.create(bind=engine, checkfirst=True)
except Exception as error:
    print(f"No se pudo verificar/crear la tabla pqr: {error}")

# 2. CREACIÓN DE LA APLICACIÓN
app = FastAPI(lifespan=lifespan)

app.title = "API chatbotbarber"
app.description = "API de gestión"
app.version = "1.0.0"

# 3. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. VERSIÓN API
API_PREFIX = "/api/v1"

# 8. ROUTES
app.include_router(disponibilidad_routes, prefix=API_PREFIX)
app.include_router(usuario_routes, prefix=API_PREFIX)
app.include_router(servicios_routes, prefix=API_PREFIX)
app.include_router(servi_dispo_routes, prefix=API_PREFIX)
app.include_router(detalle_routes, prefix=API_PREFIX)
app.include_router(agenda_routes, prefix=API_PREFIX)
app.include_router(factura_routes, prefix=API_PREFIX)
app.include_router(reporte_routes, prefix=API_PREFIX)
app.include_router(pqr_routes, prefix=API_PREFIX)


# 7. INICIO
@app.get("/")
def inicio():
    return {
        "status": True,
        "mensaje": "API chatbotbarber funcionano",
        "data": {
            "version": "v1",
            "api": "/api/v1"
        },
        "error": None,
        "code": 200
    }
