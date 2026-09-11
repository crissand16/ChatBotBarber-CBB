
from typing import Any, Optional

from datetime import date, datetime, time

from decimal import Decimal

from fastapi.responses import JSONResponse

from sqlalchemy.engine import Result


# =========================================================
# CONVERTIR DATOS A FORMATO JSON
# =========================================================

def convertir_json(data: Any):

    # -----------------------------------------------------
    # DICCIONARIO
    # -----------------------------------------------------

    if isinstance(data, dict):

        return {
            key: convertir_json(value)
            for key, value in data.items()
        }

    # -----------------------------------------------------
    # LISTA / TUPLA
    # -----------------------------------------------------

    if isinstance(data, (list, tuple)):

        return [
            convertir_json(item)
            for item in data
        ]

    # -----------------------------------------------------
    # FECHA Y HORA
    # -----------------------------------------------------

    if isinstance(
        data,
        (datetime, date, time)
    ):

        return data.isoformat()

    # -----------------------------------------------------
    # DECIMAL / NUMERIC DE POSTGRESQL
    # -----------------------------------------------------

    if isinstance(data, Decimal):

        return float(data)

    # -----------------------------------------------------
    # OTROS TIPOS
    # -----------------------------------------------------

    return data


# =========================================================
# RESPUESTA EXITOSA
# =========================================================

def response_success(

    mensaje: str,

    data: Any = None,

    code: int = 200

):

    return JSONResponse(

        status_code=code,

        content={

            "status": True,

            "mensaje": mensaje,

            "data": convertir_json(data),

            "error": None,

            "code": code

        }

    )


# =========================================================
# RESPUESTA DE ERROR
# =========================================================

def response_error(

    mensaje: str,

    error: Optional[str] = None,

    code: int = 400,

    data: Any = None

):

    return JSONResponse(

        status_code=code,

        content={

            "status": False,

            "mensaje": mensaje,

            "data": convertir_json(data),

            "error": error,

            "code": code

        }

    )

def estructurar_agendas(resultado: Result) -> list:
#Agrupa las filas devueltas por SQL unificando múltiples servicios
#pertenecientes a una misma agenda.
      
    agendas_dict = {}

    for row in resultado:
        item = dict(row._mapping)
        id_agenda = item["id_agenda"]

#.get() sirve para extraer el valor de una clave de forma segura
#gestiona la falta de información sin romper la ejecución del código

# Si la agenda no ha sido procesada, se crea el objeto base con Cliente y Especialista
        if id_agenda not in agendas_dict:
            agendas_dict[id_agenda] = {
                "id_agenda": id_agenda,
                "estado_agenda": item["estado_agenda"],
                "precio_total": float(item["precio_total"]) if item.get("precio_total") is not None else 0.0,
                "fecha_creacion_agenda": item["fecha_creacion_agenda"].isoformat() if item.get("fecha_creacion_agenda") is not None else None,
                "fecha_agenda": str(item["fecha_disponibilidad"]) if item.get("fecha_disponibilidad") else None,
                "hora_agenda": str(item["hora_inicio_disponibilidad"]) if item.get("hora_inicio_disponibilidad") else None,
                "cliente": {
                    "id": item["id_cliente"],
                    "nombre": f"{item['nombres_cliente']} {item['apellidos_cliente']}".strip()
                },
                "especialista": {
                    "id": item["id_especialista"],
                    "nombre": f"{item['nombres_especialista']} {item['apellidos_especialista']}".strip()
                },
                "servicios": []
            }

# Se agrega el servicio a la lista de servicios de esta agenda
        agendas_dict[id_agenda]["servicios"].append({
            "id_servicio": item["id_servicios"],
            "nombre": item["nombre_servicio"],
            "precio": float(item["precio_servicio"]) if item.get("precio_servicio") is not None else 0.0
        })

    return list(agendas_dict.values())

