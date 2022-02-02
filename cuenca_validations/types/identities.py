import datetime as dt
import re
from typing import Optional

from pydantic import BaseModel
from pydantic.types import StrictStr
from pydantic.validators import IPv4Address

from .enums import Country, KYCFileType, State


class PhoneNumber(StrictStr):
    min_length = 10
    max_length = 15
    regex = re.compile(r'^\+?[0-9]{10,14}$')


class CurpField(StrictStr):
    min_length = 18
    max_length = 18
    regex = re.compile(r'^[A-Z]{4}[0-9]{6}[A-Z]{6}[A-Z|0-9][0-9]$')


class Rfc(StrictStr):
    min_length = 12
    max_length = 13


class Address(BaseModel):
    street: str
    ext_number: str
    postal_code: str
    state: State
    country: Country
    city: Optional[str] = None
    int_number: Optional[str] = None


class Beneficiary(BaseModel):
    name: str
    birth_date: dt.datetime
    phone_number: PhoneNumber
    user_relationship: str
    percentage: int


class KYCFile(BaseModel):
    type: KYCFileType
    is_mx: bool
    uri_front: str
    uri_back: Optional[str] = None
    data: Optional[dict] = None


class TOSAgreement(BaseModel):
    version: str
    ip: IPv4Address
    location: str
