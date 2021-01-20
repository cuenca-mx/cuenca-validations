import datetime as dt
from typing import Optional, Union

from clabe import Clabe
from pydantic import BaseModel, Extra, StrictStr, validator
from stdnum import mx  # type: ignore

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
    date: dt.date
    document_type: DocumentType

    @validator('rfc')
    def check_rfc(cls, rfc_value: str) -> str:
        if not mx.rfc.is_valid(rfc_value):
            raise ValueError('Invalid rfc format')
        return rfc_value

    @validator('date', pre=True)
    def set_date(cls, date: Union[tuple, str]) -> dt.date:
        if isinstance(date, tuple):
            return dt.date(date[0], date[1], 1)
        return dt.datetime.strptime(date, '%Y-%m-%d').date()

    @validator('date')
    def check_date(cls, date_value: dt.date) -> dt.date:
        date_now = dt.date.today()
        if (
            date_value.year == date_now.year
            and date_value.month == date_now.month
        ):
            raise ValueError('You cannot check the current month')
        return date_value
