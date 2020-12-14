from datetime import date
from typing import Optional, Union

from clabe import Clabe
from pydantic import BaseModel, Extra, StrictStr, validator
from stdnum.mx import rfc

from ..types.enums import CardStatus, DocumentType
from .card import PaymentCardNumber, StrictPaymentCardNumber
from .general import StrictPositiveInt


class TransferRequest(BaseModel):
    recipient_name: StrictStr
    account_number: Union[Clabe, PaymentCardNumber]
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    idempotency_key: str  # must be unique for each transfer


class StrictTransferRequest(TransferRequest):
    account_number: Union[Clabe, StrictPaymentCardNumber]


class CardUpdateRequest(BaseModel):
    user_id: Optional[str]
    ledger_account_id: Optional[str]
    status: Optional[CardStatus]

    class Config:
        extra = Extra.forbid


class CardRequest(BaseModel):
    user_id: str
    ledger_account_id: str


class DocumentRequest(BaseModel):
    client_name: str
    clabe: Clabe
    address: str
    rfc: str
    date: tuple
    document_type: DocumentType

    @validator('rfc')
    def check_rfc(cls, rfc_value: str):
        if not rfc.is_valid(rfc_value):
            raise ValueError('Invalid rfc format')
        return rfc_value

    @validator('date')
    def check_date(cls, date_tuple: tuple):
        date_now = date.today()
        date_value = date(date_tuple[0], date_tuple[1], 1)
        if (
            date_value.year == date_now.year
            and date_value.month == date_now.month
        ):
            raise ValueError('You cannot check the current month')
        return date_value
