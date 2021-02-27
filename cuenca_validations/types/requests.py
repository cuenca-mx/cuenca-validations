from typing import Optional, Union

from clabe import Clabe
from pydantic import BaseModel, Extra, StrictStr, constr

from ..types.enums import CardStatus
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


class ApiKeyUpdateRequest(BaseRequest):
    user_id: Optional[str]
    metadata: Optional[DictStrAny]


class PasswordRequest(BaseRequest):
    password: constr(
        strip_whitespace=True,
        strict=True,
        min_length=6,
        max_length=6,
        regex=r'\d{6}',  # noqa: F722
    )
