from typing import Union

from clabe import Clabe
from pydantic import BaseModel, StrictStr

from .general import PaymentCardNumber, StrictPositiveInt


class TransferRequest(BaseModel):
    recipient_name: StrictStr
    account_number: Union[Clabe, PaymentCardNumber]
    amount: StrictPositiveInt  # in centavos
    descriptor: StrictStr  # how it'll appear for the recipient
    idempotency_key: str  # must be unique for each transfer
