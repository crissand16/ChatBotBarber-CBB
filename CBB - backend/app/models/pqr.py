from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    CheckConstraint,
    func,
    false
)

from app.config.database import Base


class Pqr(Base):

    __tablename__ = "pqr"

    id_pqr = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Usuario que radica la PQR
    id_usuario = Column(
        String(10),
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    nombre_pqr = Column(
        String(100),
        nullable=False
    )

    # Correo al que el administrador responderá
    correo_pqr = Column(
        String(60),
        nullable=False
    )

    tipo_pqr = Column(
        String(15),
        nullable=False
    )

    asunto_pqr = Column(
        String(120),
        nullable=False
    )

    mensaje_pqr = Column(
        Text,
        nullable=False
    )

    estado_pqr = Column(
        String(20),
        nullable=False,
        server_default="recibida"
    )

    # True cuando la notificación llegó al correo del administrador
    correo_enviado_pqr = Column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    fecha_creacion_pqr = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "tipo_pqr IN ('peticion', 'queja', 'reclamo')",
            name="chk_pqr_tipo"
        ),
        CheckConstraint(
            "estado_pqr IN ('recibida', 'en_proceso', 'respondida', 'cerrada')",
            name="chk_pqr_estado"
        ),
    )

    # Número de radicado que ve el usuario (PQR-000012)
    @property
    def radicado(self) -> str:
        return f"PQR-{self.id_pqr:06d}"

    def __repr__(self):
        return f"<Pqr id={self.id_pqr} tipo={self.tipo_pqr}>"
