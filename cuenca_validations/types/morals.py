import datetime as dt
from typing import Optional

from pydantic import BaseModel, EmailStr

from cuenca_validations.types import Address, Curp, PhoneNumber, Rfc


class BusinessDetails(BaseModel):
    business_description: str
    account_usage_description: str


class TransactionalProfileServices(BaseModel):
    spei_transfers_num: int
    spei_transfers_amount: int
    internal_transfers_num: int
    internal_transfers_amount: int


class TransactionalProfile(BaseModel):
    currency: str
    monthly_amount: int
    payers_num: int
    recipients_num: int
    deposits: Optional[TransactionalProfileServices] = None
    withdrawal: Optional[TransactionalProfileServices] = None


class LicenseDetails(BaseModel):
    license_required: bool
    supervisory_entity: Optional[str] = None
    license_type: Optional[str] = None
    license_date: Optional[dt.date] = None


class AuditDetails(BaseModel):
    has_audit: bool
    audit_provider: Optional[str] = None
    audit_date: Optional[dt.date] = None
    audit_comments: Optional[str] = None


class VulnerableActivityDetails(BaseModel):
    is_vulnerable_activity: bool
    has_sat_register: Optional[bool] = None
    sat_registered_date: Optional[dt.date] = None
    is_in_compliance: Optional[bool] = None


class PhysicalPerson(BaseModel):
    names: str
    first_surname: str
    second_surname: Optional[str] = None
    curp: Optional[Curp] = None
    rfc: Optional[Rfc] = None


class LegalRepresentative(PhysicalPerson):
    job: str
    phone_number: PhoneNumber
    email_address: EmailStr
    address: Address


class ShareholderPhysical(PhysicalPerson):
    share_capital: int


class Shareholder(BaseModel):
    name: str
    percentage: int
    shareholders: list[ShareholderPhysical]
    legal_representatives: list[LegalRepresentative]
