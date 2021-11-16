import datetime as dt
from typing import Optional

from pydantic.dataclasses import dataclass

from .enums import KYCFileType

# pasar a rquests?


@dataclass
class Address:
    created_at: dt.datetime
    calle: str
    numero_ext: str
    numero_int: Optional[str]
    codigo_postal: str
    estado: str
    ciudad: Optional[str]
    colonia: str


@dataclass
class Beneficiary:
    name: str
    birth_date: dt.datetime
    phone_number: str
    user_relationship: str
    percentage: int


@dataclass
class BlacklistValidation:
    id: str
    created_at: dt.datetime
    feedme_uri: Optional[str]
    value: Optional[str]
    deactivated_at: Optional[dt.datetime]
    status: str


@dataclass
class KYCFile:
    created_at: dt.datetime
    updated_at: dt.datetime
    type: KYCFileType
    feedme_uri_front: str
    feedme_uri_back: str
    is_mx: bool
    data: Optional[str]


@dataclass
class TOSAgreement:
    created_at: dt.datetime
    version: int
    ip: str
    location: str
    type: str  # hay que definir bien
