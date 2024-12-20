import datetime as dt
import re
from typing import Any, Dict, List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    IPvAnyAddress,
    model_validator,
)
from pydantic.types import StrictStr

from .enums import Country, KYCFileType, State, VerificationStatus


class PhoneNumber(StrictStr):
    min_length = 10
    max_length = 15
    regex = re.compile(r'^\+?[0-9]{10,14}$')

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> Dict[str, Any]:
        return {
            'type': 'str',
            'pattern': cls.regex.pattern,
            'min_length': cls.min_length,
            'max_length': cls.max_length,
        }


class CurpField(StrictStr):
    min_length = 18
    max_length = 18
    regex = re.compile(r'^[A-Z]{4}[0-9]{6}[A-Z]{6}[A-Z|0-9][0-9]$')

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> Dict[str, Any]:
        return {
            'type': 'str',
            'pattern': cls.regex.pattern,
            'min_length': cls.min_length,
            'max_length': cls.max_length,
        }


class Rfc(StrictStr):
    min_length = 12
    max_length = 13

    @classmethod
    def validate(cls, rfc: str):
        if len(rfc) < cls.min_length or len(rfc) > cls.max_length:
            raise ValueError('Not a valid RFC.')
        return cls(rfc)


class Address(BaseModel):
    street: Optional[str] = None
    ext_number: Optional[str] = None
    int_number: Optional[str] = None
    colonia: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[State] = None
    country: Optional[Country] = None
    city: Optional[str] = None
    full_name: Optional[str] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "street": "Reforma",
                "ext_number": "265",
                "int_number": "5",
                "colonia": "Cuauhtémoc",
                "postal_code": "06500",
                "state": "DF",
                "country": "MX",
                "city": "Cuauhtémoc",
            }
        }
    )

    @model_validator(mode='before')
    @classmethod
    def full_name_complete(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get('full_name'):
            return values
        if not values.get('street'):
            raise ValueError('required street')
        if not values.get('ext_number'):
            raise ValueError('required ext_number')
        return values


class Beneficiary(BaseModel):
    name: str
    birth_date: dt.date
    phone_number: PhoneNumber
    user_relationship: str
    percentage: int
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Perez",
                "birth_date": "1907-07-06",
                "phone_number": "+525500998877",
                "user_relationship": "friend",
                "percentage": 100,
            }
        }
    )


class VerificationErrors(BaseModel):
    identifier: str = Field(
        ..., description='Unique identifier for the step validation'
    )
    error: str = Field(
        ...,
        description='Error throwed on validation,'
        ' can be StepError or SystemError in case of '
        'KYCProvider intermittence',
    )
    code: str = Field(
        ..., description='Specific code of the failure in the step.'
    )
    message: Optional[str] = Field(None, description='Error description')
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "identifier": "age-check",
                "error": 'StepError',
                "code": "underage.noDOB",
                "message": "The date of birth could not be obtained",
            }
        },
    )


class KYCFile(BaseModel):
    type: KYCFileType
    uri_front: str = Field(..., description='API uri to fetch the file')
    uri_back: Optional[str] = Field(
        None, description='API uri to fetch the file'
    )
    is_mx: bool = True
    data: Optional[dict] = None
    status: Optional[VerificationStatus] = Field(
        None, description='The status of the file depends on KYCValidation'
    )
    errors: Optional[List[VerificationErrors]] = Field(
        None, description='List of document errors found during kyc validation'
    )
    verification_id: Optional[str] = Field(
        None, description='The provider identifier of the validation result'
    )
    attempt: Optional[int] = Field(
        None,
        description='The number of kyc_validation intents for this document',
    )
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "ine",
                "is_mx": True,
                "uri_front": "/files/FILE-01",
                "uri_back": "/files/FILE-02",
                "data": {},
                "status": "created",
                "errors": [],
            }
        },
    )


class TOSAgreement(BaseModel):
    version: str
    ip: IPvAnyAddress
    location: Optional[str] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "version": "2022-01-01",
                "ip": "192.168.0.1",
                "location": "19.427224, -99.168082",
            }
        }
    )
