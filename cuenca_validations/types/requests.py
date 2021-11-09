import datetime as dt
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
from pydantic.class_validators import validator

from ..types.enums import (
    AuthorizerTransaction,
    CardDesign,
    CardFundingType,
    CardholderVerificationMethod,
    CardIssuer,
    CardIssuerType,
    CardPackaging,
    CardStatus,
    CardType,
    EcommerceIndicator,
    GovtIdType,
    IssuerNetwork,
    PosCapability,
    SavingCategory,
    TrackDataMethod,
    TransactionTokenValidationStatus,
    UserCardNotification,
    UserDataType,
    UserProofType,
    WalletTransactionType,
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
    pin_attempts_exceeded: Optional[bool] = None


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
    atm_fee: Optional[StrictPositiveInt]
    issuer: IssuerNetwork
    cardholder_verification_method: Optional[CardholderVerificationMethod]
    ecommerce_indicator: Optional[EcommerceIndicator]
    fraud_validation_id: Optional[str]


class UserCardNotificationRequest(CardTransactionRequest):
    type: UserCardNotification


class SavingBaseRequest(BaseRequest):
    goal_amount: Optional[StrictPositiveInt]
    goal_date: Optional[dt.datetime]

    @validator('goal_date')
    def validate_goal_date(
        cls, v: Optional[dt.datetime]
    ) -> Optional[dt.datetime]:
        if v and v <= dt.datetime.utcnow():
            raise ValueError('The goal_date always need to be higher than now')
        return v


class SavingRequest(SavingBaseRequest):
    name: str
    category: SavingCategory


class SavingUpdateRequest(SavingBaseRequest):
    name: Optional[str]
    category: Optional[SavingCategory]


class WalletTransactionRequest(BaseRequest):
    wallet_uri: str
    transaction_type: WalletTransactionType
    amount: StrictPositiveInt


class FraudValidationRequest(BaseModel):
    amount: StrictPositiveInt
    merchant_name: str
    merchant_type: str
    merchant_data: str
    currency_code: str
    transaction_type: AuthorizerTransaction
    track_data_method: TrackDataMethod
    pos_capability: PosCapability
    logical_network: Optional[str]
    is_cvv: Optional[bool] = False
    issuer: IssuerNetwork
    cardholder_verification_method: Optional[CardholderVerificationMethod]
    ecommerce_indicator: Optional[EcommerceIndicator]
    card_id: Optional[str]  # type: ignore
    user_id: Optional[str]  # type: ignore
    card_type: Optional[CardType]  # type: ignore
    card_status: Optional[CardStatus]  # type: ignore


class TransactionTokenValidationUpdateRequest(BaseRequest):
    status: TransactionTokenValidationStatus


class UserPldRiskLevelRequest(BaseModel):
    user_id: str
    level: float = Field(ge=0.0, le=1.0)


class AddressRequest(BaseModel):
    user_id: Optional[str]
    calle: str
    numero_ext: str
    codigo_postal: str
    estado: str
    colonia: str
    ciudad: Optional[str] = None
    numero_int: Optional[str] = None

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        extra = 'allow'


class UserProofRequest(BaseModel):
    user_id: Optional[str]
    type: UserProofType
    feedme_uri: str


class UserDataRequest(BaseModel):
    user_id: Optional[str]
    type: UserDataType
    data: str


class BeneficiaryRequest(BaseModel):
    user_id: Optional[str]
    name: str
    birth_date: dt.datetime
    phone_number: str
    user_relationship: str
    percentage: int


class GovtIDRequest(BaseModel):
    user_uri: Optional[str]
    type: GovtIdType
    is_mx: bool
    feedme_uri: str
    number: Optional[str] = None


class TOSAgreementRequest(BaseModel):
    user_id: Optional[str]
    version: int
    ip: str
    location: str
    type: CardIssuerType


class UserRequest(BaseModel):
    nombres: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[str] = None
    birth_country: Optional[str] = None
    pronouns: Optional[str] = None
    curp: Optional[str] = None

    # estos son para en caso de que se mande de un jalón
    address: Optional[AddressRequest] = None
    phone_number: Optional[UserDataRequest] = None
    email_address: Optional[UserDataRequest] = None
    terms: Optional[TOSAgreementRequest] = None
    profession: Optional[UserDataRequest] = None
    proof_of_address: Optional[UserProofRequest] = None
    proof_of_life: Optional[UserProofRequest] = None
    govt_id: Optional[GovtIDRequest] = None

    @validator(
        'nombres', 'primer_apellido', 'gender', 'birth_place', 'birth_date'
    )
    def segundo_apellido_opcional(cls, segundo_value):
        if len(segundo_value) <= 0:
            raise ValueError('Length must be greater than 0')
        return segundo_value

    class Config:
        anystr_strip_whitespace = True


class HumanRequest(UserRequest):
    user_id: Optional[str]
