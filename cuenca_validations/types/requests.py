import datetime as dt
from typing import List, Optional, Union

from clabe import Clabe
from pydantic import (
    AnyUrl,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    StrictStr,
    StringConstraints,
    field_validator,
    model_validator,
)
from pydantic.networks import IPvAnyAddress
from typing_extensions import Annotated

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
    FileExtension,
    Gender,
    IssuerNetwork,
    KYCFileType,
    PlatformType,
    PosCapability,
    SavingCategory,
    SessionType,
    State,
    TermsOfService,
    TrackDataMethod,
    TransactionTokenValidationStatus,
    UserCardNotification,
    UserStatus,
    VerificationType,
    WalletTransactionType,
    WebhookEvent,
    WebhookEventType,
    WebhookObject,
)
from ..typing import DictStrAny
from ..validators import validate_age_requirement
from .card import PaymentCardNumber, StrictPaymentCardNumber
from .general import StrictPositiveInt
from .identities import (
    Address,
    Beneficiary,
    CurpField,
    KYCFile,
    PhoneNumber,
    Rfc,
    TOSAgreement,
)
from .morals import (
    AuditDetails,
    BusinessDetails,
    LegalRepresentative,
    LicenseDetails,
    Shareholder,
    TransactionalProfile,
    VulnerableActivityDetails,
)


class BaseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def dict(self, *args, **kwargs) -> DictStrAny:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_unset', True)
        return super().dict(*args, **kwargs)


class TransferRequest(BaseRequest):
    recipient_name: StrictStr
    account_number: Union[Clabe, PaymentCardNumber] = Field(
        ..., description='Destination Clabe or Card number'
    )
    amount: StrictPositiveInt = Field(
        ..., description='Always in cents, not in MXN pesos'
    )
    descriptor: StrictStr = Field(
        ..., description='Short description for the recipient'
    )
    idempotency_key: str = Field(
        ..., description='Custom Id, must be unique for each transfer'
    )
    user_id: Optional[str] = Field(
        None, description='Source user to take the funds'
    )
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'recipient_name': 'Doroteo Arango',
                'account_number': '646180157034181180',
                'amount': 100_00,  # 100.00 MXN Pesos
                'descriptor': 'Mezcal, pulque y tequila',
                'idempotency_key': 'UNIQUE-KEY-003',
                'user_id': 'USWqY5cvkISJOxHyEKjAKf8w',
            }
        },
    )


class StrictTransferRequest(BaseRequest):
    account_number: Union[Clabe, StrictPaymentCardNumber]


class CardUpdateRequest(BaseRequest):
    status: Optional[CardStatus] = None
    pin_block: Optional[str] = None
    is_dynamic_cvv: Optional[bool] = None


class CardRequest(BaseRequest):
    user_id: str = 'me'
    issuer: CardIssuer
    funding_type: CardFundingType
    is_dynamic_cvv: Optional[bool] = None
    card_holder_user_id: Optional[str] = None


class CardActivationRequest(BaseModel):
    number: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=16,
            max_length=16,
            pattern=r'\d{16}',
        ),
    ]
    exp_month: Annotated[int, Field(strict=True, ge=1, le=12)]  # type: ignore
    exp_year: Annotated[int, Field(strict=True, ge=18, le=99)]  # type: ignore
    cvv2: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=3,
            pattern=r'\d{3}',
        ),
    ]


class ApiKeyUpdateRequest(BaseRequest):
    user_id: Optional[str] = None
    platform_id: Optional[str] = None
    metadata: Optional[DictStrAny] = None


class UserCredentialUpdateRequest(BaseRequest):
    is_active: Optional[bool] = None
    password: Optional[str] = Field(
        None,
        min_length=6,
        max_length=128,
        description=(
            'Any str with at least 6 characters, maximum 128 characters'
        ),
    )

    def dict(self, *args, **kwargs) -> DictStrAny:
        # Password can be None but BaseRequest excludes None
        return BaseModel.dict(self, *args, **kwargs)

    @model_validator(mode="before")
    @classmethod
    def check_one_property_at_a_time(cls, values: DictStrAny) -> DictStrAny:
        not_none_count = sum(1 for val in values.values() if val)
        if not_none_count > 1:
            raise ValueError('Only one property can be updated at a time')
        return values


class UserCredentialRequest(BaseRequest):
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description=(
            'Any str with at least 6 characters, maximum 128 characters'
        ),
    )
    user_id: Optional[str] = None


class CardValidationRequest(BaseModel):
    number: Annotated[
        str,
        StringConstraints(
            min_length=16,
            max_length=16,
            pattern=r'\d{16}',
            strip_whitespace=True,
        ),
    ]
    exp_month: Optional[Annotated[int, Field(strict=True, ge=1, le=12)]] = None
    exp_year: Optional[Annotated[int, Field(strict=True, ge=18, le=99)]] = None
    cvv: Optional[  # type: ignore
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, strict=True, min_length=3, max_length=3
            ),
        ]
    ] = None
    cvv2: Optional[  # type: ignore
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, strict=True, min_length=3, max_length=3
            ),
        ]
    ] = None
    icvv: Optional[  # type: ignore
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, strict=True, min_length=3, max_length=3
            ),
        ]
    ] = None
    pin_block: Optional[
        Annotated[str, StringConstraints(strip_whitespace=True)]
    ] = None
    pin_attempts_exceeded: Optional[bool] = None


class ARPCRequest(BaseModel):
    number: Annotated[
        str,
        StringConstraints(
            min_length=16,
            max_length=16,
            pattern=r'\d{16}',
            strip_whitespace=True,
        ),
    ]
    arqc: StrictStr
    arpc_method: Annotated[
        str,
        StringConstraints(  # type: ignore
            strict=True, min_length=1, max_length=1
        ),
    ]
    transaction_data: StrictStr
    response_code: StrictStr
    transaction_counter: StrictStr
    pan_sequence: StrictStr
    unique_number: StrictStr
    track_data_method: TrackDataMethod


class CardBatchRequest(BaseRequest):
    card_design: CardDesign
    card_packaging: CardPackaging
    number_of_cards: Annotated[int, Field(strict=True, ge=1, le=999999)]


class CardTransactionRequest(BaseModel):
    card_id: str
    user_id: str
    # In some card_validations amount is equal to 0
    amount: Annotated[int, Field(strict=True, ge=0)]  # type: ignore
    merchant_name: str
    merchant_type: str
    merchant_data: str
    currency_code: str
    prosa_transaction_id: str
    retrieval_reference: str
    card_type: CardType
    card_status: CardStatus
    transaction_type: AuthorizerTransaction
    authorizer_number: Optional[str] = None


class ReverseRequest(CardTransactionRequest):
    ...


class CardNotificationRequest(CardTransactionRequest):
    track_data_method: TrackDataMethod
    pos_capability: PosCapability
    logical_network: Optional[str] = None


class ChargeRequest(CardNotificationRequest):
    is_cvv: Optional[bool] = False
    get_balance: Optional[bool] = False
    atm_fee: Optional[StrictPositiveInt] = None
    issuer: IssuerNetwork
    cardholder_verification_method: Optional[
        CardholderVerificationMethod
    ] = None
    ecommerce_indicator: Optional[EcommerceIndicator] = None
    fraud_validation_id: Optional[str] = None


class UserCardNotificationRequest(CardTransactionRequest):
    type: UserCardNotification


class SavingBaseRequest(BaseRequest):
    goal_amount: Optional[StrictPositiveInt] = None
    goal_date: Optional[dt.datetime] = None

    @field_validator('goal_date')
    @classmethod
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
    name: Optional[str] = None
    category: Optional[SavingCategory] = None


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
    logical_network: Optional[str] = None
    is_cvv: Optional[bool] = False
    issuer: IssuerNetwork
    cardholder_verification_method: Optional[
        CardholderVerificationMethod
    ] = None
    ecommerce_indicator: Optional[EcommerceIndicator] = None
    card_id: Optional[str] = None  # type: ignore
    user_id: Optional[str] = None  # type: ignore
    card_type: Optional[CardType] = None  # type: ignore
    card_status: Optional[CardStatus] = None  # type: ignore


class TransactionTokenValidationUpdateRequest(BaseRequest):
    status: TransactionTokenValidationStatus


class UserPldRiskLevelRequest(BaseModel):
    user_id: str
    level: float = Field(ge=0.0, le=1.0)


class CurpValidationRequest(BaseModel):
    names: Optional[str] = None
    first_surname: Optional[str] = None
    second_surname: Optional[str] = Field(
        None, description='Not necessary for foreigners'
    )
    date_of_birth: Optional[dt.date] = None
    state_of_birth: Optional[State] = Field(
        None, description='In format ISO 3166 Alpha-2'
    )
    country_of_birth: Optional[Country] = Field(
        None, description='In format ISO 3166 Alpha-2'
    )
    gender: Optional[Gender] = None
    manual_curp: Optional[CurpField] = Field(
        None,
        description='Force to validate this curp instead of use '
        'the one we calculate',
    )
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            'example': {
                'names': 'Guillermo',
                'first_surname': 'Gonzales',
                'second_surname': 'Camarena',
                'date_of_birth': '1965-04-18',
                'state_of_birth': 'VZ',
                'country_of_birth': 'MX',
                'gender': 'male',
            }
        },
    )

    @field_validator('second_surname')
    @classmethod
    def validate_surname(cls, value: Optional[str]) -> Optional[str]:
        return value if value else None  # Empty strings as None

    @field_validator('date_of_birth')
    @classmethod
    def validate_birth_date(
        cls, date_of_birth: Optional[dt.date]
    ) -> Optional[dt.date]:
        try:
            validate_age_requirement(date_of_birth) if date_of_birth else None
        except ValueError:
            raise
        return date_of_birth

    @model_validator(mode="before")
    @classmethod
    def validate_state_of_birth(cls, values: DictStrAny) -> DictStrAny:
        if (
            'country_of_birth' in values
            and values['country_of_birth'] == 'MX'
            and 'state_of_birth' not in values
        ):
            raise ValueError('state_of_birth required')
        return values

    @model_validator(mode="before")
    @classmethod
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


class TOSRequest(BaseModel):
    type: TermsOfService
    version: str
    location: Optional[str] = None
    ip: Optional[IPvAnyAddress] = None


class UserRequest(BaseModel):
    id: Optional[str] = Field(
        None, description='if you want to create with specific `id`'
    )
    curp: CurpField = Field(
        ..., description='Previously validated in `curp_validations`'
    )
    phone_number: Optional[PhoneNumber] = Field(
        None, description='Only if you validated previously on your side'
    )
    email_address: Optional[EmailStr] = Field(
        None, description='Only if you validated previously on your side'
    )
    profession: Optional[str] = None
    address: Optional[Address] = None
    status: Optional[UserStatus] = Field(
        None,
        description='Status that the user will have when created. '
        'Defined by platform',
    )
    required_level: Optional[Annotated[int, Field(ge=-1, le=4)]] = Field(
        None,
        description='Maximum level a User can reach. ' 'Defined by platform',
    )
    phone_verification_id: Optional[str] = Field(
        None,
        description='Only if you validated it previously with the '
        'resource `verifications`',
    )
    email_verification_id: Optional[str] = Field(
        None,
        description='Only if you validated it previously with the '
        'resource `verifications`',
    )
    terms_of_service: Optional[TOSRequest] = None
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'curp': 'GOCG650418HVZNML08',
                'phone_number': '+525511223344',
                'email_address': 'user@example.com',
                'profession': 'engineer',
                'address': Address.schema().get('example'),
            }
        },
    )

    @field_validator('curp')
    @classmethod
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


class UserUpdateRequest(BaseModel):
    phone_number: Optional[PhoneNumber] = None
    email_address: Optional[EmailStr] = None
    profession: Optional[str] = None
    verification_id: Optional[str] = None
    email_verification_id: Optional[str] = None
    phone_verification_id: Optional[str] = None
    address: Optional[Address] = None
    beneficiaries: Optional[List[Beneficiary]] = None
    govt_id: Optional[KYCFile] = None
    proof_of_address: Optional[KYCFile] = None
    proof_of_life: Optional[KYCFile] = None
    status: Optional[UserStatus] = None
    terms_of_service: Optional[TOSRequest] = None
    platform_terms_of_service: Optional[TOSAgreement] = None
    curp_document_uri: Optional[HttpUrl] = None

    @field_validator('beneficiaries')
    @classmethod
    def beneficiary_percentage(
        cls, beneficiaries: Optional[List[Beneficiary]] = None
    ):
        if beneficiaries and sum(b.percentage for b in beneficiaries) > 100:
            raise ValueError('The total percentage is more than 100.')
        return beneficiaries


class UserLoginRequest(BaseRequest):
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description=(
            'Any str with at least 6 characters, maximum 128 characters'
        ),
    )
    user_id: Optional[str] = Field(None, description='Deprecated field')
    model_config = ConfigDict(
        json_schema_extra={'example': {'password': 'supersecret'}},
    )


class SessionRequest(BaseRequest):
    user_id: str
    type: SessionType
    success_url: Optional[AnyUrl] = None
    failure_url: Optional[AnyUrl] = None
    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'user_id': 'USWqY5cvkISJOxHyEKjAKf8w',
                'type': 'session.registration',
                'success_url': 'http://example_success.com',
                'failure_url': 'http://example_failure.com',
            }
        }
    )


class EndpointRequest(BaseRequest):
    url: HttpUrl
    events: Optional[List[WebhookEvent]] = None
    user_id: Optional[str] = None


class EndpointUpdateRequest(BaseRequest):
    url: Optional[HttpUrl] = None
    is_enable: Optional[bool] = None
    events: Optional[List[WebhookEvent]] = None


class FileUploadRequest(BaseRequest):
    is_back: Optional[bool] = False
    file: Union[bytes, str]
    extension: Optional[FileExtension] = None
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
    recipient: Union[EmailStr, PhoneNumber] = Field(
        description='Phone or email to validate'
    )
    platform_id: str
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            'example': {
                'type': 'email',
                'recipient': 'user@example.com',
                'platform_id': 'PT8UEv02zBTcymd4Kd3MO6pg',
            }
        },
    )

    @field_validator('recipient')
    def validate_sender(cls, recipient: str, values):
        return (
            EmailStr(recipient)
            if type == VerificationType.email
            else PhoneNumber(recipient)
        )


class VerificationAttemptRequest(BaseModel):
    code: Annotated[
        str,
        StringConstraints(strict=True, min_length=6, max_length=6),
        Field(description="Code sent to user via email or phone"),
    ]
    model_config = ConfigDict(
        json_schema_extra={'example': {'code': '123456'}},
    )


class LimitedWalletRequest(BaseRequest):
    model_config = dict(arbitrary_types_allowed=True)

    allowed_curp: CurpField
    allowed_rfc: Optional[Rfc] = None


class KYCVerificationUpdateRequest(BaseRequest):
    curp: CurpField


class PlatformRequest(BaseModel):
    model_config = dict(arbitrary_types_allowed=True)
    name: str
    rfc: Optional[str] = None
    establishment_date: Optional[dt.date] = None
    country: Optional[Country] = None
    state: Optional[State] = None
    economic_activity: Optional[str] = None
    phone_number: Optional[str] = None
    email_address: Optional[str] = None
    type: PlatformType = PlatformType.connect


class WebhookRequest(BaseModel):
    id: str
    event: WebhookEventType
    object_type: WebhookObject
    data: DictStrAny


class KYCValidationRequest(BaseRequest):
    user_id: str
    force: bool = False
    documents: List[KYCFile] = []


class BankAccountValidationRequest(BaseModel):
    account_number: Union[Clabe, PaymentCardNumber]


class UserListsRequest(BaseModel):
    curp: Optional[CurpField] = Field(
        None, description='Curp to review on lists'
    )
    account_number: Optional[Union[Clabe, PaymentCardNumber]] = Field(
        None, description='Account to review on lists'
    )
    names: Optional[str] = Field(
        None, description='Names of the user to review on lists'
    )
    first_surname: Optional[str] = Field(
        None, description='first_surname of the user to review on lists'
    )
    second_surname: Optional[str] = Field(
        None, description='second_surname of the user to review on lists'
    )

    @model_validator(mode='before')
    @classmethod
    def check_request(cls, values):
        has_name = all(values.get(f) for f in ['names', 'first_surname'])
        curp, account = values.get('curp'), values.get('account_number')
        if not any([curp, account, has_name]):
            raise ValueError("At least 1 param is required")
        return values

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            'example': {
                'curp': 'GOCG650418HVZNML08',
                'account_number': '9203929392939292392',
                'names': 'Pedrito',
                'first_surname': 'Sola',
                'second_surname': 'Sola',
            }
        },
    )


class QuestionnairesRequest(BaseModel):
    user_id: str
    token: str
    form_id: str


class PartnerRequest(BaseRequest):
    model_config = dict(arbitrary_types_allowed=True)

    legal_name: str
    business_name: str
    nationality: Country
    incorporation_date: dt.date
    folio: str
    rfc: Rfc
    documentation_url: str
    web_site: str
    phone_number: PhoneNumber
    email_address: EmailStr
    address: Address


class PartnerUpdateRequest(BaseRequest):
    model_config = dict(arbitrary_types_allowed=True)

    legal_name: Optional[str] = None
    business_name: Optional[str] = None
    nationality: Optional[Country] = None
    incorporation_date: Optional[dt.date] = None
    folio: Optional[str] = None
    rfc: Optional[Rfc] = None
    documentation_url: Optional[str] = None
    web_site: Optional[str] = None
    phone_number: Optional[PhoneNumber] = None
    email_address: Optional[EmailStr] = None
    address: Optional[Address] = None
    business_details: Optional[BusinessDetails] = None
    transactional_profile: Optional[TransactionalProfile] = None
    external_account: Optional[Clabe] = None
    license: Optional[LicenseDetails] = None
    audit: Optional[AuditDetails] = None
    vulnerable_activity: Optional[VulnerableActivityDetails] = None
    legal_representatives: Optional[List[LegalRepresentative]] = None
    shareholders: Optional[List[Shareholder]] = None
