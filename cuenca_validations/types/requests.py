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
    card_id: StrictStr
    arqc: StrictStr  # type: ignore
    key_derivation_method: constr(  # type: ignore
        strict=True, min_length=1, max_length=1
    )
    arpc_method: constr(  # type: ignore
        strict=True, min_length=1, max_length=1
    )
    txn_data: StrictStr  # type: ignore
    master_key_derivation_mode: StrictStr = ''  # type: ignore
    pan_sequence: constr(  # type: ignore
        strict=True, min_length=2, max_length=2
    ) = ''
    atc: StrictStr = ''  # type: ignore
    unique_number: StrictStr = ''  # type: ignore
    arc: StrictStr = ''  # type: ignore
    card_status_update: StrictStr = ''  # type: ignore
    proprietary_data: StrictStr = ''  # type: ignore
    derivation_parameters: StrictStr = ''  # type: ignore
    derivation_iv: StrictStr = ''  # type: ignore
    master_key_derivation_data: StrictStr = ''  # type: ignore
    padding: StrictStr = ''  # type: ignore
