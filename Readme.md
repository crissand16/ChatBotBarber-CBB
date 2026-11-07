# 🚀 CBB - Backend (ChatBot Barber)

Este repositorio contiene el backend del proyecto **ChatBot Barber**, desarrollado con **FastAPI** y configurado para ejecutarse en contenedores **Docker**, optimizado para un flujo de trabajo ágil y de recarga en caliente en entorno de desarrollo.

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura modular separada por responsabilidades dentro del directorio principal del backend:

```text
CBB - backend/
│
├── app/                  # Núcleo de la aplicación FastAPI
│   ├── config/           # Configuraciones generales
│   ├── controllers/      # Lógica de negocio / controladores
│   ├── models/           # Modelos de base de datos (SQLAlchemy)
│   ├── routes/           # Endpoints de la API
│   ├── schema/           # Esquemas de validación de datos (Pydantic)
│   ├── utils/            # Funciones de apoyo o utilidades
│   ├── __init__.py
│   └── main.py           # Punto de entrada de FastAPI
│
├── database/             # Archivos o scripts relacionados con la base de datos
├── .dockerignore         # Archivos ignorados por Docker
├── .env                  # Variables de entorno
├── Dockerfile            # Configuración de la imagen de Docker
├── docker-compose.yml    # Orquestador de contenedores para desarrollo
└── requirements.txt      # Dependencias de Python

⚙️ Funcionamiento y Esquema de Docker
Para entender cómo interactúa tu máquina local con el contenedor en tiempo de desarrollo, observa el siguiente esquema:

┌─────────────────────────────────────────────────────────┐
 │               MÁQUINA LOCAL (Tu Computadora)            │
 │                                                         │
 │   Tu Código Local (app/, requirements.txt, etc.)        │
 │         │                                               │
 │         │  (Mapeo de Volúmenes: . ──> /app)             │
 └─────────┼───────────────────────────────────────────────┘
           │
           ▼
 ┌─────────────────────────────────────────────────────────┐
 │               CONTENDOR DOCKER (Aislado)                │
 │                                                         │
 │   📁 Directorio de Trabajo: /app                        │
 │   🐍 Entorno Python 3.11 + Librerías (requirements.txt) │
 │   🔄 Uvicorn Server (con `--reload` activo)             │
 │                                                         │
 │   * Si editas un archivo localmente, Uvicorn lo detecta │
 │     y reinicia la app al instante sin reconstruir.      │
 └─────────────────────────────────────────────────────────┘

 Entorno Contenerizado: Todo el ecosistema (Python, dependencias del sistema como libpq-dev para PostgreSQL y librerías de Python) corre dentro de un contenedor Docker aislado.

Sincronización en Tiempo Real (Volúmenes): Gracias al mapeo de volúmenes en el docker-compose.yml, cualquier cambio que hagas en tu equipo se refleja de inmediato dentro de la ruta /app del contenedor.

Recarga en Caliente (--reload): Uvicorn detecta los cambios en el código de forma automática, aplicando las modificaciones sin necesidad de ejecutar un docker build.

🛠️ Comandos Útiles para Cada Tarea
A continuación tienes la lista de comandos de Docker Compose que utilizarás en tu día a día:

1. Iniciar el entorno por primera vez (o tras modificar dependencias)
Usa este comando si es la primera vez que levantas el proyecto o si agregaste una nueva librería a tu requirements.txt:

Bash
docker compose up --build
2. Iniciar el entorno en el día a día (Modo normal)
Una vez creado el contenedor inicial, para trabajar diariamente solo ejecuta:

Bash
docker compose up
3. Detener los contenedores
Para apagar la aplicación de forma limpia cuando termines de programar:

Bash
docker compose down
4. Ver los logs en tiempo real
Si necesitas depurar errores o ver el comportamiento de las peticiones HTTP de la API:

Bash
docker compose logs -f
🌐 Endpoints y Documentación
Una vez que el contenedor esté corriendo con éxito, puedes acceder a las interfaces interactivas de la API:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc