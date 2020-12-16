from typing import Optional, Union

from clabe import Clabe
from pydantic import BaseModel, Extra, StrictStr

from ..types.enums import CardStatus
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
