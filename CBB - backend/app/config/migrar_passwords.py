from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def migrar_passwords(db: Session):
  # 1. Obtener todos los usuarios de la base de datos
  usuarios = db.query(Usuario).all()

  actualizados = 0
  omitidos = 0

  for usuario in usuarios:
    contrasena_actual = usuario.contrasena_usuario

    # 2. Verificar si la contraseña ya está hasheada
    if contrasena_actual.startswith("$2b"):
      omitidos += 1
      continue

    # 3. Si está en texto plano, generar el hash
    nuevo_hash = pwd_context.hash(contrasena_actual)

    # 4. Asignar el hash al usuario
    usuario.contrasena_usuario = nuevo_hash
    actualizados += 1

  # 5. Guardar los cambios en la BD de forma masiva
  try:
    db.commit()
    print("---- Migración finalizada ----")
    print(f"Contraseñas actualizadas a hash: {actualizados}")
    print(f"Contraseñas que ya estaban hasheadas: {omitidos}")
  except Exception as e:
    db.rollback()
    print(f"Ocurrió un error y se hizo rollback: {e}")


if __name__ == "__main__":
  db = SessionLocal()  # Aquí se abre la BD
  try:
    migrar_passwords(db)
  finally:
    db.close()  # Cierra la sesión al terminar