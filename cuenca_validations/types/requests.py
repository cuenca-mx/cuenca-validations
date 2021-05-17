from typing import Optional, Union

from clabe import Clabe
from pydantic import (
    BaseModel,
    Extra,
    Field,
    StrictStr,
    conint,
    constr,
    root_validator,
)

from ..types.enums import (
    AuthorizerTransaction,
    CardDesign,
    CardFundingType,
    CardIssuer,
    CardPackaging,
    CardStatus,
    CardType,
    PosCapability,
    TrackDataMethod,
    UserCardNotification,
)
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
    status: Optional[CardStatus]
    pin_block: Optional[str]


class CardRequest(BaseRequest):
    user_id: str = 'me'
    issuer: CardIssuer
    funding_type: CardFundingType


class CardActivationRequest(BaseModel):
    number: str = Field(
        ...,
        strip_whitespace=True,
        min_length=16,
        max_length=16,
        regex=r'\d{16}',
    )
    exp_month: conint(strict=True, ge=1, le=12)  # type: ignore
    exp_year: conint(strict=True, ge=18, le=99)  # type: ignore
    cvv2: str = Field(
        ..., strip_whitespace=True, min_length=3, max_length=3, regex=r'\d{3}'
    )


class ApiKeyUpdateRequest(BaseRequest):
    user_id: Optional[str]
    metadata: Optional[DictStrAny]


class UserCredentialUpdateRequest(BaseRequest):
    is_active: Optional[bool]
    password: Optional[str] = Field(
        None, max_length=6, min_length=6, regex=r'\d{6}'
    )

    def dict(self, *args, **kwargs) -> DictStrAny:
        # Password can be None but BaseRequest excludes None
        return BaseModel.dict(self, *args, **kwargs)

    @root_validator(pre=True)
    def check_one_property_at_a_time(cls, values: DictStrAny) -> DictStrAny:
        not_none_count = sum(1 for val in values.values() if val)
        if not_none_count > 1:
            raise ValueError('Only one property can be updated at a time')
        return values


class UserCredentialRequest(BaseRequest):
    password: str = Field(..., max_length=6, min_length=6, regex=r'\d{6}')


class CardValidationRequest(BaseModel):
    number: str = Field(
        ...,
        strip_whitespace=True,
        min_length=16,
        max_length=16,
        regex=r'\d{16}',
    )
    exp_month: Optional[conint(strict=True, ge=1, le=12)]  # type: ignore
    exp_year: Optional[conint(strict=True, ge=18, le=99)]  # type: ignore
    cvv: Optional[  # type: ignore
        constr(strip_whitespace=True, strict=True, min_length=3, max_length=3)
    ]
    cvv2: Optional[  # type: ignore
        constr(strip_whitespace=True, strict=True, min_length=3, max_length=3)
    ]
    icvv: Optional[  # type: ignore
        constr(strip_whitespace=True, strict=True, min_length=3, max_length=3)
    ]
    pin_block: Optional[constr(strip_whitespace=True)] = None  # type: ignore


class ARPCRequest(BaseModel):
    number: str = Field(
        ...,
        strip_whitespace=True,
        min_length=16,
        max_length=16,
        regex=r'\d{16}',
    )
    arqc: StrictStr
    arpc_method: constr(  # type: ignore
        strict=True, min_length=1, max_length=1
    )
    transaction_data: StrictStr
    response_code: StrictStr
    transaction_counter: StrictStr
    pan_sequence: StrictStr
    unique_number: StrictStr
    track_data_method: TrackDataMethod


class CardBatchRequest(BaseRequest):
    card_design: CardDesign
    card_packaging: CardPackaging
    number_of_cards: conint(strict=True, ge=1, le=999999)  # type: ignore


class CardTransactionRequest(BaseModel):
    card_id: str
    user_id: str
    amount: StrictPositiveInt
    merchant_name: str
    merchant_type: str
    merchant_data: str
    currency_code: str
    prosa_transaction_id: str
    retrieval_reference: str
    card_type: CardType
    card_status: CardStatus
    transaction_type: AuthorizerTransaction
    authorizer_number: Optional[str]


class ReverseRequest(CardTransactionRequest):
    ...


class CardNotificationRequest(CardTransactionRequest):
    track_data_method: TrackDataMethod
    pos_capability: PosCapability
    logical_network: Optional[str]


class ChargeRequest(CardNotificationRequest):
    is_cvv: Optional[bool] = False
    get_balance: Optional[bool] = False


class UserCardNotificationRequest(CardTransactionRequest):
    type: UserCardNotification
