import datetime as dt
import re
from typing import Any, Dict, Optional

from pydantic import BaseModel
from pydantic.class_validators import root_validator
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
    street: Optional[str] = None
    ext_number: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[State] = None
    country: Optional[Country] = None
    city: Optional[str] = None
    int_number: Optional[str] = None
    full_name: Optional[str] = None

    @root_validator()
    def full_name_complete(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get('full_name') and not values.get('street'):
            raise ValueError('required street')
        if not values.get('full_name') and not values.get('ext_number'):
            raise ValueError('required ext_number')
        if not values.get('full_name') and not values.get('state'):
            raise ValueError('required state')
        if not values.get('full_name') and not values.get('country'):
            raise ValueError('required country')
        return values


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
    location: Optional[str]
