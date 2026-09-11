from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


from app.config.settings import DATABASE_URL


engine = create_engine( #Gestiona la conexión eficiente con la base de datos
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)


SessionLocal = sessionmaker( #Crea las sesiones para realizar consultas
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db(): #Garantiza que las conexiones se cierren tras cada petición en tus endpoints

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()