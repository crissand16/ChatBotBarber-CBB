"""Excepciones de negocio que las rutas traducen a códigos HTTP.

Heredan de ValueError para que el código existente que captura
ValueError (400) siga funcionando sin cambios.
"""


class NoEncontrado(ValueError):
    """El recurso solicitado no existe (HTTP 404)."""


class Conflicto(ValueError):
    """La operación choca con el estado actual de los datos (HTTP 409)."""
