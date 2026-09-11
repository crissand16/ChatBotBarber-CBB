from sqlalchemy import text
from app.config.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Usuario, Agenda, Disponibilidad, Servicios, ServicioDisponibilidadCreate, DetalleCreate


try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("Conexión exitosa a la base de datos")
except Exception as error:
    print(f"Error de conexión a la base de datos: {error}")

# 2. CREACIÓN DE LA APLICACIÓN
app = FastAPI(
    title="API chatbotbarber",
    description="API de gestión",
    version="1.0.0"
)

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

# 4. IMPORTAR ROUTES
from app.routes.usuario_routes import (
    router as usuario_routes
)

from app.routes.disponibilidad_routes import (
    router as disponibilidad_routes
)

from app.routes.servicios_routes import (
    router as servicios_routes
)

from app.routes.servi_dispo_routes import (
    router as servi_dispo_routes
)

from app.routes.detalle_routes import (
    router as detalle_routes
)

from app.routes.agenda_routes import (
    router as agenda_routes
)

# 5. VERSIÓN API
API_PREFIX = "/api/v1"

# 6. ROUTES

app.include_router(
    disponibilidad_routes, 
    prefix=API_PREFIX)

app.include_router(
    usuario_routes, 
    prefix=API_PREFIX)

app.include_router(
    servicios_routes, 
    prefix=API_PREFIX)

app.include_router(
    servi_dispo_routes, 
    prefix=API_PREFIX)

app.include_router(
    detalle_routes, 
    prefix=API_PREFIX)

app.include_router(
    agenda_routes, 
    prefix=API_PREFIX)

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