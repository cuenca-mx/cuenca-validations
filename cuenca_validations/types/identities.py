import datetime as dt
import re
from typing import Optional

from pydantic.dataclasses import dataclass

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


class PhoneNumber(str):
    phone_number_regex = re.compile(r'^\+[0-9]{12}$')

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError
        m = cls.phone_number_regex.fullmatch(v)
        if not m:
            raise ValueError('invalid phone number format')
        return m.string
