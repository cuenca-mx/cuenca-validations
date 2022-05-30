import datetime as dt
from ipaddress import AddressValueError
from typing import Dict, List, Optional, Union

from clabe import Clabe
from pydantic import (
    AnyUrl,
    BaseModel,
    EmailStr,
    Extra,
    Field,
    HttpUrl,
    StrictStr,
    conint,
    constr,
    root_validator,
)
from pydantic.class_validators import validator
from pydantic.validators import IPv4Address

from ..types.enums import (
    AuthorizerTransaction,
    CardDesign,
    CardFundingType,
    CardholderVerificationMethod,
    CardIssuer,
    CardPackaging,
    CardStatus,
    CardType,
    Country,
    EcommerceIndicator,
    Gender,
    IssuerNetwork,
    KYCFileType,
    PosCapability,
    SavingCategory,
    SessionType,
    State,
    TrackDataMethod,
    TransactionTokenValidationStatus,
    UserCardNotification,
    VerificationType,
    WalletTransactionType,
    WebhookEvent,
)
from ..typing import DictStrAny
from ..validators import validate_age_requirement
from .card import PaymentCardNumber, StrictPaymentCardNumber
from .general import StrictPositiveInt
from .identities import (
    Address,
    Beneficiary,
    CurpField,
    PhoneNumber,
    Rfc,
    TOSAgreement,
)


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
    amount: StrictPositiveInt
    descriptor: StrictStr
    idempotency_key: str

    class Config:
        fields = {
            'account_number': {
                'description': 'Destination Clabe or Card number'
            },
            'amount': {'description': 'Always in cents, not in MXN pesos'},
            'descriptor': {
                'description': "Short description for the recipient"
            },
            'idempotency_key': {
                'description': 'Custom Id, must be unique for each transfer'
            },
        }
        schema_extra = {
            "example": {
                "recipient_name": 'Doroteo Arango',
                "account_number": "646180157034181180",
                "amount": 10000,  # 100.00 MXN Pesos
                "descriptor": "Mezcal, pulque y tequila",
                "idempotency_key": "UNIQUE-KEY-003",
            }
        }


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
    user_id: Optional[str] = None
    platform_id: Optional[str] = None
    metadata: Optional[DictStrAny] = None


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


class CurpValidationRequest(BaseModel):
    names: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = None
    date_of_birth: Optional[dt.date] = None
    state_of_birth: Optional[State] = None
    country_of_birth: Optional[Country] = None
    gender: Optional[Gender] = None
    manual_curp: Optional[CurpField] = None

    class Config:
        anystr_strip_whitespace = True
        fields = {
            'second_surname': {'description': 'Not neccessary for foreigners'},
            'country_of_birth': {'description': 'In format ISO 3166 Alpha-2'},
            'state_of_birth': {'description': 'In format ISO 3166 Alpha-2'},
            'nationality': {'description': 'In format ISO 3166 Alpha-2'},
            'manual_curp': {
                'description': 'Force to validate this curp instead of use '
                'the one we calculate'
            },
        }
        schema_extra = {
            "example": {
                "names": "Guillermo",
                "first_surname": "Gonzales",
                "second_surname": "Camarena",
                "date_of_birth": "1965-04-18",
                "state_of_birth": "VZ",
                "country_of_birth": "MX",
                "gender": "male",
            }
        }

    @validator('second_surname')
    def validate_surname(cls, value: Optional[str]) -> Optional[str]:
        return value if value else None  # Empty strings as None

    @validator('date_of_birth')
    def validate_birth_date(
        cls, date_of_birth: Optional[dt.date]
    ) -> Optional[dt.date]:
        try:
            validate_age_requirement(date_of_birth) if date_of_birth else None
        except ValueError:
            raise
        return date_of_birth

    @root_validator(pre=True)
    def validate_state_of_birth(cls, values: DictStrAny) -> DictStrAny:
        if (
            'country_of_birth' in values
            and values['country_of_birth'] == 'MX'
            and 'state_of_birth' not in values
        ):
            raise ValueError('state_of_birth required')
        return values

    @root_validator(pre=True)
    def validate_manual_curp(cls, values: DictStrAny) -> DictStrAny:
        manual_curp = values.get('manual_curp')
        required = [
            'names',
            'first_surname',
            'date_of_birth',
            'country_of_birth',
            'gender',
        ]
        missing = [r for r in required if r not in values.keys()]
        if not manual_curp and missing:
            raise ValueError(f'values required: {",".join(missing)}')
        return values


class UserRequest(BaseModel):
    curp: CurpField
    phone_number: Optional[PhoneNumber] = None
    email_address: Optional[EmailStr] = None
    profession: Optional[str] = None
    address: Optional[Address] = None
    phone_verification_id: Optional[str] = None
    email_verification_id: Optional[str] = None

    class Config:
        fields = {
            'curp': {
                'description': 'Previously validated in curp_validations'
            },
            'phone_number': {'description': 'Validated for you'},
            'email_address': {'description': 'Validated for you'},
            'phone_verification_id': {
                'description': 'Only if you validate phone with resource '
                'verifications'
            },
            'email_verification_id': {
                'description': 'Only if you validate email with resource '
                'verifications'
            },
        }
        schema_extra = {
            "example": {
                "curp": "GOCG650418HVZNML08",
                "phone_number": "+525511223344",
                "email_address": "user@example.com",
                "profession": "engineer",
                "address": Address.schema().get('example'),
            }
        }

    @validator('curp')
    def validate_birth_date(
        cls, curp: Optional[CurpField]
    ) -> Optional[CurpField]:
        if curp:
            current_date = dt.datetime.utcnow()
            curp_date = curp[4:10]
            century = (
                '19'
                if int(curp_date[:2]) > int(str(current_date.year)[:2])
                else '20'
            )
            birth_date = dt.datetime.strptime(century + curp_date, '%Y%m%d')
            try:
                validate_age_requirement(birth_date)
            except ValueError:
                raise
        return curp


class AddressUpdateRequest(BaseModel):
    street: Optional[str] = None
    ext_number: Optional[str] = None
    int_number: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[State] = None
    city: Optional[str] = None
    country: Optional[Country] = None


class TOSUpdateRequest(BaseModel):
    version: Optional[str] = None
    ip: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None

    @validator('ip')
    def validate_ip(cls, ip: str):
        # we validate ip address this way because the
        # model IPv4Address is not JSON serializable
        try:
            IPv4Address(ip)
        except AddressValueError:
            raise ValueError('not valid ip')
        return ip


class KYCFileUpdateRequest(BaseModel):
    type: Optional[KYCFileType] = None
    uri_front: Optional[str] = None
    uri_back: Optional[str] = None
    is_mx: Optional[bool] = None
    data: Optional[Dict] = None


class UserUpdateRequest(BaseModel):
    phone_number: Optional[PhoneNumber] = None
    email_address: Optional[EmailStr] = None
    profession: Optional[str] = None
    verification_id: Optional[str] = None
    address: Optional[AddressUpdateRequest] = None
    beneficiaries: Optional[List[Beneficiary]] = None
    govt_id: Optional[KYCFileUpdateRequest] = None
    proof_of_address: Optional[KYCFileUpdateRequest] = None
    proof_of_life: Optional[KYCFileUpdateRequest] = None
    terms_of_service: Optional[TOSUpdateRequest] = None
    platform_terms_of_service: Optional[TOSAgreement] = None

    @validator('beneficiaries')
    def beneficiary_percentage(
        cls, beneficiaries: Optional[List[Beneficiary]] = None
    ):
        if beneficiaries and sum(b.percentage for b in beneficiaries) != 100:
            raise ValueError(
                'The total percentage of beneficiaries does not add 100.'
            )
        return beneficiaries


class UserLoginRequest(BaseRequest):
    password: str

    class Config:
        fields = {'password': {'description': 'Customer password'}}
        schema_extra = {"example": {"password": "supersecret"}}


class SessionRequest(BaseRequest):
    user_id: str
    type: SessionType
    success_url: Optional[AnyUrl] = None
    failure_url: Optional[AnyUrl] = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "US-123",
                "type": "session.registration",
                "success_url": "http://example_success.com",
                "failure_url": "http://example_failure.com",
            }
        }


class EndpointRequest(BaseRequest):
    url: HttpUrl
    events: Optional[List[WebhookEvent]]


class EndpointUpdateRequest(BaseRequest):
    url: Optional[HttpUrl]
    is_enable: Optional[bool]
    events: Optional[List[WebhookEvent]]


class FileUploadRequest(BaseRequest):
    is_back: Optional[bool] = False
    file: Union[bytes, str]
    extension: Optional[str]
    type: KYCFileType
    user_id: str


class FileRequest(BaseModel):
    is_back: Optional[bool] = False
    url: HttpUrl
    type: KYCFileType


class FileBatchUploadRequest(BaseModel):
    files: List[FileRequest]
    user_id: str


class VerificationRequest(BaseModel):
    type: VerificationType
    recipient: Union[EmailStr, PhoneNumber]
    platform_id: str

    class Config:
        anystr_strip_whitespace = True

    @validator('recipient')
    def validate_sender(cls, recipient: str, values):
        return (
            EmailStr(recipient)
            if type == VerificationType.email
            else PhoneNumber(recipient)
        )


class VerificationAttemptRequest(BaseModel):
    code: constr(strict=True, min_length=6, max_length=6)  # type: ignore


class LimitedWalletRequest(BaseRequest):
    allowed_curp: CurpField
    allowed_rfc: Optional[Rfc]


class IdentityUpdateRequest(BaseRequest):
    rfc_file: bytes
    user_id: str
    extension: str


class KYCVerificationUpdateRequest(BaseRequest):
    curp: CurpField
