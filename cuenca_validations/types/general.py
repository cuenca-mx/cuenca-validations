import json
from typing import Generator, Optional

from pydantic import BeforeValidator, Field
from typing_extensions import Annotated

from ..validators import sanitize_dict, sanitize_item
from .enums import State


class SantizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return sanitize_item(o, default=super().default)


def validate_strict_positive_int(value: int) -> int:
    if not isinstance(value, int):
        raise ValueError("Value must be an integer")
    if value <= 0:
        raise ValueError("Value must be greater than 0")
    if value > 21_474_836_47:
        raise ValueError("Value must be less than 21_474_836_47")
    return value


StrictPositiveInt = Annotated[
    int, BeforeValidator(validate_strict_positive_int)
]


def validate_strict_positive_float(value: float) -> float:
    if not isinstance(value, float):
        raise ValueError("Value must be a float")
    if value <= 0:
        raise ValueError("Value must be greater than 0")
    return value


StrictPositiveFloat = Annotated[
    float, BeforeValidator(validate_strict_positive_float)
]


# Clase base para validación
class Digits:
    min_length: Optional[int] = None
    max_length: Optional[int] = None

    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate_digits

    @classmethod
    def validate_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Value must contain only digits.")
        if cls.min_length is not None and len(value) < cls.min_length:
            raise ValueError(
                f"Value must have at least {cls.min_length} characters."
            )
        if cls.max_length is not None and len(value) > cls.max_length:
            raise ValueError(
                f"Value must have at most {cls.max_length} characters."
            )
        return value


# Función para crear tipos personalizados
def digits(min_length: Optional[int] = None, max_length: Optional[int] = None):
    return Annotated[
        str, Field(min_length=min_length, max_length=max_length), Digits
    ]


names_state = {
    State.NE: 'Nacido en el Extranjero',
    State.AS: 'Aguascalientes',
    State.BC: 'Baja California',
    State.BS: 'Baja California Sur',
    State.CC: 'Campeche',
    State.CS: 'Chiapas',
    State.CH: 'Chihuahua',
    State.CL: 'Coahuila',
    State.CM: 'Colima',
    State.DF: 'Ciudad de México',
    State.DG: 'Durango',
    State.GT: 'Guanajuato',
    State.GR: 'Guerrero',
    State.HG: 'Hidalgo',
    State.JC: 'Jalisco',
    State.MC: 'México',
    State.MN: 'Michoacan',
    State.MS: 'Morelos',
    State.NT: 'Nayarit',
    State.NL: 'Nuevo León',
    State.OC: 'Oaxaca',
    State.PL: 'Puebla',
    State.QT: 'Querétaro',
    State.QR: 'Quintana Roo',
    State.SP: 'San Luis Potosí',
    State.SL: 'Sinaloa',
    State.SR: 'Sonora',
    State.TC: 'Tabasco',
    State.TL: 'Tlaxcala',
    State.TS: 'Tamaulipas',
    State.VZ: 'Veracruz',
    State.YN: 'Yucatán',
    State.ZS: 'Zacatecas',
}


def get_state_name(state: State):
    return names_state[state]
