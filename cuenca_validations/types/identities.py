import datetime as dt
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, SecretStr, StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber

from .enums import Country, KYCFileType, State, VerificationStatus
from .general import NonEmptyStr, SerializableIPvAnyAddress

Password = Annotated[
    SecretStr,
    Field(
        min_length=8,
        max_length=128,
        description=(
            'Any str with at least 8 characters, maximum 128 characters'
        ),
    ),
]

Curp = Annotated[
    str,
    StringConstraints(
        min_length=18,
        max_length=18,
        pattern=r'^[A-Z]{4}[0-9]{6}[A-Z]{6}[A-Z|0-9][0-9]$',
    ),
]


Rfc = Annotated[
    str,
    StringConstraints(
        min_length=12,
        max_length=13,
    ),
]

# NOTE:
# The Address model is kept for compatibility with legacy models and data
# that expect all address fields to be optional. This allows older systems
# or stored data using Address to continue working without breaking changes.
# For new request validation, use AddressRequest, which enforces required
# fields and is intended for validating incoming data.


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


class AddressRequest(BaseModel):
    # This model is mainly for request validation, enforcing required fields.
    street: NonEmptyStr
    ext_number: NonEmptyStr
    int_number: Optional[NonEmptyStr] = None
    postal_code_id: NonEmptyStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "street": "Reforma",
                "ext_number": "265",
                "int_number": "5",
                "postal_code_id": "PC2ygq9j2bS9-9tsuVawzErA",
            }
        }
    )


class Beneficiary(BaseModel):
    name: str
    birth_date: dt.date
    phone_number: PhoneNumber
    user_relationship: str
    percentage: Annotated[int, Field(ge=1, le=100)]
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
        description='Unique identifier for the step validation'
    )
    error: str = Field(
        description='Error throwed on validation,'
        ' can be StepError or SystemError in case of '
        'KYCProvider intermittence',
    )
    code: str = Field(description='Specific code of the failure in the step.')
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
    uri_front: str = Field(description='API uri to fetch the file')
    uri_back: Optional[str] = Field(
        None, description='API uri to fetch the file'
    )
    is_mx: bool = True
    data: Optional[dict] = None
    status: Optional[VerificationStatus] = Field(
        None, description='The status of the file depends on KYCValidation'
    )
    errors: Optional[list[VerificationErrors]] = Field(
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
                "data": {
                    "location": "19.432608, -99.133209",
                    "ip": "192.168.1.100",
                    "hash": "a1b2c3d4e5f67890abcdef1234567890",
                },
                "status": "created",
                "errors": [],
            }
        },
    )


class TOSAgreement(BaseModel):
    version: str
    ip: SerializableIPvAnyAddress
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
