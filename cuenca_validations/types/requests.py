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


class IndentityRequest(BaseModel):
    id: str
    rfc: str
    user_id: str
    created_at: str
    curp_status: str
    gov_id_count: int
    gov_id_status: str
    black_list_validation: Optional[dict]
    black_lists_status: Optional[str]
    ine_validation: Optional[dict]
    mati_identity: Optional[dict]
    proof_of_address_status: str
    selfie_status: str
    selfie_video_count: int
    selfie_video_status: str
