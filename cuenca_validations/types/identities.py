import datetime as dt
import re
from typing import Optional

from pydantic import BaseModel
from pydantic.types import StrictStr

from .enums import KYCFileType, States


class Address(BaseModel):
    calle: str
    numero_ext: str
    codigo_postal: str
    estado: States
    colonia: str
    ciudad: Optional[str] = None
    numero_int: Optional[str] = None


class Beneficiary(BaseModel):
    name: str
    birth_date: dt.datetime
    phone_number: str
    user_relationship: str
    percentage: int


class KYCFile(BaseModel):
    type: KYCFileType
    is_mx: bool
    feedme_uri_front: str
    feedme_uri_back: Optional[str] = None
    data: Optional[dict] = None


class TOSAgreement(BaseModel):
    version: int
    ip: str
    location: str
    type: str  # hay que definir bien


class PhoneNumber(StrictStr):
    min_length = 10
    max_length = 13
    regex = re.compile(r'^\+{0,1}[0-9]{10,12}$')


class Curp(StrictStr):
    min_length = 18
    max_length = 18
    regex = re.compile(r'^[A-Z]{4}[0-9]{6}[A-Z]{6}[A-Z|0-9][0-9]$')


class Rfc(StrictStr):
    min_length = 12
    max_length = 13
