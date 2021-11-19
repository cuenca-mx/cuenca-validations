import datetime as dt
import re
from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic.types import StrictStr

from .enums import KYCFileType, States


@dataclass
class Address:
    created_at: dt.datetime
    calle: str
    numero_ext: str
    numero_int: Optional[str]
    codigo_postal: str
    estado: States
    ciudad: Optional[str]
    colonia: str


@dataclass
class Beneficiary:
    name: str
    birth_date: dt.datetime
    phone_number: str
    user_relationship: str
    percentage: int
    created_at: dt.datetime


@dataclass
class KYCFile:
    created_at: dt.datetime
    type: KYCFileType
    feedme_uri_front: str
    feedme_uri_back: Optional[str]
    is_mx: bool
    data: Optional[dict]


@dataclass
class TOSAgreement:
    created_at: dt.datetime
    version: int
    ip: str
    location: str
    type: str  # hay que definir bien


class PhoneNumber(StrictStr):
    min_length = 10
    max_length = 12
    regex = re.compile(r'^\+[0-9]{12}$')


class Curp(StrictStr):
    min_length = 18
    max_length = 18
    regex = re.compile(r'^[A-Z]{4}[0-9]{6}[A-Z]{6}[A-Z|0-9][0-9]$')


class Rfc(StrictStr):
    min_length = 12
    max_length = 13
