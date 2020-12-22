from typing import Optional, Union

from clabe import Clabe
from pydantic import BaseModel, Extra, StrictStr

from ..types.enums import CardStatus, CardIssuer, CardFundingType
from ..typing import DictStrAny
from .card import PaymentCardNumber, StrictPaymentCardNumber
from .general import StrictPositiveInt


class BaseRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    def dict(self, *args, **kwargs) -> DictStrAny:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_unset', True)
        return super().dict(*args, **kwargs)


class TransferRequest(BaseRequest):
    recipient_name: StrictStr
    account_number: Union[Clabe, PaymentCardNumber]
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    idempotency_key: str  # must be unique for each transfer


class StrictTransferRequest(TransferRequest):
    account_number: Union[Clabe, StrictPaymentCardNumber]


class CardUpdateRequest(BaseRequest):
    user_id: Optional[str]
    ledger_account_id: Optional[str]
    status: Optional[CardStatus]


class CardRequest(BaseRequest):
    user_id: str
    ledger_account_id: str
    issuer: CardIssuer
    funding_type: CardFundingType


class ApiKeyUpdateRequest(BaseRequest):
    user_id: Optional[str]
    metadata: Optional[DictStrAny]
