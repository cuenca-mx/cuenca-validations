import datetime as dt
from typing import Optional

from pydantic.dataclasses import dataclass

from .enums import KYCFileType, States

# pasar a rquests?


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
class BlacklistValidation:
    created_at: dt.datetime
    status: str


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
