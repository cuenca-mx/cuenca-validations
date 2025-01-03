import json
from typing import Any, Optional

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


MAX_VALUE_IN_DB = 21_474_836_47

StrictPositiveInt = Annotated[
    int, Field(strict=True, gt=0, le=MAX_VALUE_IN_DB)
]


StrictPositiveFloat = Annotated[float, Field(strict=True, gt=0)]


def validate_only_digits(value: str) -> str:
    if not value.isdigit():
        raise ValueError("Value must contain only digits")
    return value


def digits(
    min_length: Optional[int] = None, max_length: Optional[int] = None
) -> Any:
    return Annotated[
        str,
        BeforeValidator(validate_only_digits),
        Field(min_length=min_length, max_length=max_length),
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
