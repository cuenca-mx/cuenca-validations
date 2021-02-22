from typing import Optional, Union

from clabe import Clabe
from pydantic import BaseModel, Extra, StrictStr, conint, constr

from ..types.enums import CardFundingType, CardIssuer, CardStatus
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
    status: CardStatus


class CardRequest(BaseRequest):
    user_id: str = 'me'
    issuer: CardIssuer
    funding_type: CardFundingType


class CardActivationRequest(BaseModel):
    number: StrictStr
    exp_month: conint(strict=True, ge=1, le=12)  # type: ignore
    exp_year: conint(strict=True, ge=18, le=99)  # type: ignore
    cvv2: constr(  # type: ignore
        strip_whitespace=True, strict=True, min_length=3, max_length=3
    )
    issuer: CardIssuer
    funding_type: CardFundingType


class ApiKeyUpdateRequest(BaseRequest):
    user_id: Optional[str]
    metadata: Optional[DictStrAny]
