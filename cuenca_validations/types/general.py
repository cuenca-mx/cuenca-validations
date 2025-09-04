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
from .enums import (
    AccountUseType,
    IncomeType,
    MonthlyMovementsType,
    MonthlySpendingType,
    Profession,
    State,
)

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
    State.MN: 'Michoacán',
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


def get_state_name(state: State) -> str:
    return names_state[state]


names_professions = {
    Profession.artisticas: 'Actividades Artísticas',
    Profession.agropecuario: 'Agricultura, Ganadería o Pesca',
    Profession.comercio: 'Comercio',
    Profession.estudiante: 'Estudiante',
    Profession.empleado: 'Empleado(a/e)',
    Profession.emprendimiento: 'Emprendimiento',
    Profession.hogar: 'Hogar',
    Profession.profesor: 'Profesor(a/e)',
    Profession.profesionista: 'Profesionista',
    Profession.servidor_publico: 'Servidor(a/e) Público',
    Profession.sistemas: 'Sistemas y Comunicaciones',
    Profession.independiente: 'Trabajador(a/e) Independiente',
    Profession.oficios: 'Oficios Varios',
    Profession.otro: 'Otro',
}


def get_profession_name(profession: Profession) -> str:
    return names_professions[profession]


names_account_use_types = {
    AccountUseType.personal_expenses: 'Gastos personales o familiares',
    AccountUseType.business_expenses: (
        'Gastos relacionados con tu actividad económica'
    ),
    AccountUseType.payment_of_goods_or_services: 'Pago de bienes o servicios',
    AccountUseType.send_or_receive_transfers: (
        'Enviar o recibir transferencias'
    ),
}


def get_account_use_type_name(account_use_type: AccountUseType) -> str:
    return names_account_use_types[account_use_type]


names_monthly_movements_types = {
    MonthlyMovementsType.between_1_and_20: 'Entre 1 y 20 movimientos',
    MonthlyMovementsType.between_20_and_40: 'Entre 20 y 40 movimientos',
    MonthlyMovementsType.between_40_and_60: 'Entre 40 y 60 movimientos',
    MonthlyMovementsType.more_than_60: 'Más de 60 movimientos',
}


def get_monthly_movements_type_name(
    monthly_movements_type: MonthlyMovementsType,
) -> str:
    return names_monthly_movements_types[monthly_movements_type]


names_monthly_spending_types = {
    MonthlySpendingType.less_than_1k: 'Menos de $1,000',
    MonthlySpendingType.between_1k_and_10k: 'Entre $1,000 y $10,000',
    MonthlySpendingType.between_10k_and_20k: 'Entre $10,000 y $20,000',
    MonthlySpendingType.between_20k_and_50k: 'Entre $20,000 y $50,000',
    MonthlySpendingType.between_50k_and_100k: 'Entre $50,000 y $100,000',
    MonthlySpendingType.more_than_100k: 'Más de $100,000',
}


def get_monthly_spending_type_name(
    monthly_spending_type: MonthlySpendingType,
) -> str:
    return names_monthly_spending_types[monthly_spending_type]


names_income_types = {
    IncomeType.salary: 'Sueldo o salario fijo',
    IncomeType.freelance: 'Independiente',
    IncomeType.support_from_third_party: 'Apoyo de terceros o familiares',
    IncomeType.variable: 'Variable',
}


def get_income_type_name(income_type: IncomeType) -> str:
    return names_income_types[income_type]


@dataclass
class LogConfig:
    masked: bool = False
    unmasked_chars_length: int = 0
    excluded: bool = False
