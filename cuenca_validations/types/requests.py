from typing import Optional, Union

from clabe import Clabe
from pydantic import BaseModel, Extra, StrictStr, conint, constr

from ..types.enums import CardFundingType, CardIssuer, CardStatus
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
    status: Optional[CardStatus]

    class Config:
        extra = Extra.forbid


class CardRequest(BaseModel):
    user_id: str = 'me'
    issuer: CardIssuer
    funding_type: CardFundingType


class CardActivationRequest(BaseModel):
    number: str
    exp_month: conint(strict=True, ge=1, le=12)
    exp_year: conint(strict=True, ge=2018, le=2099)
    cvv2: constr(
        strip_whitespace=True, strict=True, min_length=4, max_length=4
    )
    issuer: CardIssuer
    funding_type: CardFundingType


class ApiKeyUpdateRequest(BaseModel):
    user_id: Optional[str]
    metadata: Optional[str]

    class Config:
        extra = Extra.forbid
