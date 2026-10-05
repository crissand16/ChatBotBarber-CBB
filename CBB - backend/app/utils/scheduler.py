from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from app.config.database import SessionLocal  # Importa la sesión de tu base de datos


def generar_disponibilidad_automatica():
  """Genera automáticamente disponibilidad para los especialistas a 15 días a partir de hoy

  y vincula el bloque con los servicios existentes.
  """
  db = SessionLocal()
  try:
    query = text("""
            WITH nuevas_disponibilidades AS (
                INSERT INTO disponibilidad (
                    id_especialista, 
                    fecha_disponibilidad, 
                    hora_inicio_disponibilidad, 
                    hora_fin_disponibilidad, 
                    estado_disponibilidad
                )
                SELECT 
                    id_usuario, 
                    CURRENT_DATE + INTERVAL '15 days', 
                    '10:00:00'::TIME, 
                    '11:00:00'::TIME, 
                    'disponible'
                FROM usuario 
                WHERE rol_usuario = 'especialista'
                ON CONFLICT (id_especialista, fecha_disponibilidad, hora_inicio_disponibilidad) DO NOTHING
                RETURNING id_disponibilidad
            )
            INSERT INTO servicio_disponibilidad (id_servicios, id_disponibilidad)
            SELECT 
                s.id_servicios, 
                nd.id_disponibilidad
            FROM nuevas_disponibilidades nd
            CROSS JOIN servicios s
            ON CONFLICT DO NOTHING;
        """)

    db.execute(query)
    db.commit()
    print(
        " Disponibilidad a 15 días generada/verificada automáticamente."
    )
  except Exception as e:
    db.rollback()
    print(f" Error al generar disponibilidad automática: {e}")
  finally:
    db.close()


def iniciar_scheduler():
  """Inicia el programador de tareas en segundo plano."""
  scheduler = BackgroundScheduler()

  # Programa la tarea para correr todos los días a medianoche (00:00)
  scheduler.add_job(
      generar_disponibilidad_automatica, 'cron', hour=0, minute=0
  )

  # Ejecutamos una vez al arrancar el servidor para garantizar datos actualizados
  generar_disponibilidad_automatica()

  scheduler.start()