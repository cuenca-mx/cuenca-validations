import json
from dataclasses import dataclass
from typing import Annotated, Any, Optional

from pydantic import (
    AnyUrl,
    Field,
    HttpUrl,
    IPvAnyAddress,
    PlainSerializer,
    StringConstraints,
)

from ..validators import sanitize_dict, sanitize_item
from .enums import State

# We use custom serializers for IP addresses and URLs because
# Pydantic's IPvAnyAddress, AnyUrl, HttpUrl types are not JSON serializable.
SerializableHttpUrl = Annotated[HttpUrl, PlainSerializer(str, return_type=str)]
SerializableAnyUrl = Annotated[AnyUrl, PlainSerializer(str, return_type=str)]
SerializableIPvAnyAddress = Annotated[
    IPvAnyAddress, PlainSerializer(str, return_type=str)
]

NonEmptyStr = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1)
]


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


def digits(
    min_length: Optional[int] = None, max_length: Optional[int] = None
) -> Annotated[Any, StringConstraints]:
    return Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=min_length,
            max_length=max_length,
            pattern=r'^\d+$',
        ),
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


@dataclass
class LogConfig:
    masked: bool = False
    unmasked_chars_length: int = 0
    excluded: bool = False
