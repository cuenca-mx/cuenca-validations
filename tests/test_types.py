import datetime as dt
import json
from dataclasses import dataclass
from enum import Enum
from typing import Annotated

import pytest
from freezegun import freeze_time
from pydantic import AfterValidator, BaseModel, SecretStr, ValidationError
from pydantic.fields import FieldInfo

from cuenca_validations.types import (
    Address,
    CardQuery,
    JSONEncoder,
    QueryParams,
    SantizedDict,
    SessionRequest,
    TransactionStatus,
    digits,
    get_state_name,
)
from cuenca_validations.types.enums import (
    Country,
    EcommerceIndicator,
    SessionType,
    State,
)
from cuenca_validations.types.general import LogConfig, StrictPositiveInt
from cuenca_validations.types.helpers import get_log_config
from cuenca_validations.types.identities import Password
from cuenca_validations.types.requests import (
    ApiKeyUpdateRequest,
    BankAccountValidationRequest,
    ChargeRequest,
    CurpValidationRequest,
    EndpointRequest,
    EndpointUpdateRequest,
    LimitedWalletRequest,
    SavingRequest,
    SavingUpdateRequest,
    UserCardNotificationRequest,
    UserCredentialUpdateRequest,
    UserListsRequest,
    UserRequest,
    UserUpdateRequest,
    VerificationAttemptRequest,
    VerificationRequest,
)

today = dt.date.today()
now = dt.datetime.now()
utcnow = now.astimezone(dt.timezone.utc)


class EnumModel(Enum):
    zero = 0


@dataclass
class DictModel:
    uno: str

    def to_dict(self):
        return dict(uno=self.uno, dos='dos')


def test_dict():
    model = QueryParams(count=1, created_before=now)
    assert model.model_dump() == dict(
        count=1, created_before=utcnow.isoformat()
    )


def test_dict_with_exclude():
    model = QueryParams(count=1, created_before=now, user_id='USXXXX')
    assert model.model_dump(exclude={'user_id'}) == dict(
        count=1, created_before=utcnow.isoformat()
    )


def test_dict_with_exclude_unset():
    model = QueryParams(count=1, created_before=now)
    assert model.model_dump(exclude_unset=False) == dict(
        count=1, created_before=utcnow.isoformat(), page_size=100
    )


def test_sanitized_dict():
    assert SantizedDict(
        status=TransactionStatus.succeeded,
        time=now,
        hello='there',
        dates=[now],
    ) == dict(
        status='succeeded',
        time=utcnow.isoformat(),
        hello='there',
        dates=[utcnow.isoformat()],
    )


@pytest.mark.parametrize(
    'count, truth',
    [
        (1, True),
        ('1', True),
        (True, True),
        (False, False),
        (0, False),
        ('0', False),
    ],
)
def test_count(count, truth):
    q = QueryParams(count=count)
    assert q.count is truth


@pytest.mark.parametrize(
    'value, result',
    [
        (EnumModel.zero, 0),
        (today, today.isoformat()),
        (now, utcnow.isoformat()),
        (DictModel(uno='uno'), dict(uno='uno', dos='dos')),
        (b'test', 'dGVzdA=='),  # b64 encode
    ],
)
def test_json_encoder(value, result):
    to_encode = dict(value=value)
    encoded = json.dumps(to_encode, cls=JSONEncoder)
    decoded = json.loads(encoded)

    assert decoded['value'] == result


def test_invalid_class():
    """
    For a class that doesn't have a `to_dict` method and it is not a type of
    `date` nor `Enum`, will use the default `json.JSONEncoder` method which
    raises a `TypeError`.
    """

    class ClassWithoutToDict: ...  # noqa: E701

    invalid_class = ClassWithoutToDict()
    with pytest.raises(TypeError):
        json.dumps(invalid_class, cls=JSONEncoder)


class Accounts(BaseModel):
    number: digits(5, 8)  # type: ignore


@pytest.mark.parametrize(
    "input_number, expected",
    [
        ('123456', '123456'),
        ('0012312', '0012312'),
    ],
)
def test_only_digits(input_number, expected):
    acc = Accounts(number=input_number)
    assert acc.number == expected


@pytest.mark.parametrize(
    'number, error',
    [
        (12345, 'Input should be a valid string'),
        ('123', 'String should have at least 5 characters'),
        ('1234567890', 'String should have at most 8 characters'),
        ('no_123', "String should match pattern '^\\d+$'"),
    ],
)
def test_invalid_digits(number, error):
    with pytest.raises(ValidationError) as exception:
        Accounts(number=number)
    assert error in str(exception.value)


@pytest.mark.parametrize(
    'input_value',
    [
        (dict(exp_month=1)),
        (dict(exp_year=2026)),
        (dict(cvv2='123')),
        (dict(cvv='123')),
    ],
)
def test_card_query_exp_cvv_if_number_not_set(input_value):
    with pytest.raises(ValueError):
        CardQuery(**input_value)


def test_exclude_none_in_dict():
    request = ApiKeyUpdateRequest(user_id='US123')
    assert request.model_dump() == dict(user_id='US123')


def test_update_one_property_at_a_time_request():
    with pytest.raises(ValueError):
        UserCredentialUpdateRequest(user_id='US123', password='12345678')

    req = UserCredentialUpdateRequest(password='12345678')
    assert not req.is_active and req.password.get_secret_value() == '12345678'

    req = UserCredentialUpdateRequest(is_active=True)
    assert req.is_active and not req.password


@pytest.mark.parametrize(
    'data,expected_dict',
    [
        (
            dict(password='12345678'),
            dict(password=SecretStr('12345678'), is_active=None),
        ),
        (dict(is_active=True), dict(password=None, is_active=True)),
        (dict(), dict(password=None, is_active=None)),
    ],
)
def test_update_credential_update_request_dict(data, expected_dict):
    req = UserCredentialUpdateRequest(**data)
    assert req.model_dump() == expected_dict


def test_card_transaction_requests():
    data = dict(
        card_id='CA123',
        user_id='US123',
        amount=100,
        merchant_name='visa',
        merchant_data='0279288357            00012558',
        merchant_type='wtype',
        currency_code='458',
        prosa_transaction_id='12345',
        authorizer_number='123456',
        retrieval_reference='who ks',
        transaction_type='normal_purchase',
        card_type='virtual',
        card_status='active',
        track_data_method='terminal',
        pos_capability='pin_accepted',
        is_cvv=False,
        get_balance=False,
        issuer='Mastercard',
        ecommerce_indicator='0',
    )
    ChargeRequest(**data)

    # Validate atm_fee optional
    data['atm_fee'] = 1800
    request = ChargeRequest(**data)
    assert request.ecommerce_indicator is EcommerceIndicator.not_ecommerce

    # Validate amount = 0
    data['amount'] = 0
    assert ChargeRequest(**data)

    # missing fields
    with pytest.raises(ValidationError):
        UserCardNotificationRequest(**data)

    # invalid fields
    data['atm_fee'] = -1
    with pytest.raises(ValidationError):
        ChargeRequest(**data)
    data['amount'] = -1
    with pytest.raises(ValidationError):
        UserCardNotificationRequest(**data)


def test_saving_request():
    dt_now = dt.datetime.now()
    data = dict(
        name='My car',
        category='vehicle',
        goal_amount=66600,
        goal_date=dt_now + dt.timedelta(days=1),
    )
    SavingRequest(**data)

    data['goal_amount'] = -1000
    with pytest.raises(ValidationError):
        SavingRequest(**data)

    data['goal_amount'] = 66600
    data['goal_date'] = dt_now
    with pytest.raises(ValidationError):
        SavingRequest(**data)


def test_saving_update_request():
    data = dict(
        name='Mt home ',
        category='home',
        goal_amount=1000,
    )
    SavingUpdateRequest(**data)
    data['goal_date'] = dt.datetime(2000, 1, 1)
    with pytest.raises(ValidationError):
        SavingUpdateRequest(**data)


def test_address_validation():
    data = dict(
        full_name='Varsovia 36, Col Cuahutemoc',
    )
    assert Address(**data)
    with pytest.raises(ValueError) as v:
        Address(**dict())
    assert 'required street' in str(v)
    data = dict(street='somestreet')
    with pytest.raises(ValueError) as v:
        Address(**data)
    assert 'required ext_number' in str(v)
    data = dict(
        street='varsovia',
        ext_number='36',
        state=State.DF,
        country=Country.MX,
    )
    assert Address(**data)


@freeze_time('2022-01-01')
def test_user_request():
    request = dict(
        id=None,
        curp='ABCD920604HDFSRN03',
        phone_number='+525555555555',
        email_address='email@email.com',
        profession='worker',
        status='active',
        address=dict(
            street='calle 1',
            ext_number='2',
            int_number='3',
            colonia='Juarez',
            postal_code='09900',
            state=State.DF.value,
            country=Country.MX,
            city='Obrera',
            full_name=None,
        ),
        phone_verification_id='VE12345678',
        email_verification_id='VE0987654321',
        required_level=3,
        terms_of_service=None,
        signature=None,
    )
    assert UserRequest(**request).model_dump() == request

    # changing curp so user is underage
    request['curp'] = 'ABCD060604HDFSRN03'
    with pytest.raises(ValueError) as v:
        UserRequest(**request)
        assert 'User does not meet age requirement.' in str(v)


@freeze_time('2022-01-01')
def test_curp_validation_request():
    request = dict(
        names='Pedro',
        first_surname='Páramo',
        second_surname=None,
        date_of_birth=dt.date(1917, 5, 17),
        state_of_birth=State.DF.value,
        gender='male',
        manual_curp='ABCD920604HDFSRN03',
        country_of_birth='MX',
    )

    with pytest.raises(ValueError) as v:
        CurpValidationRequest()
    # Update the assertion to check for the presence of
    # required fields in the error message
    error_msg = str(v.value)
    required_fields = [
        'names',
        'first_surname',
        'date_of_birth',
        'country_of_birth',
        'gender',
    ]
    assert all(field in error_msg for field in required_fields)

    req_curp = CurpValidationRequest(**request)
    assert req_curp.model_dump() == request

    request['date_of_birth'] = dt.date(2006, 5, 17)

    with pytest.raises(ValueError) as v:
        CurpValidationRequest(**request)
    assert 'User does not meet age requirement.' in str(v)

    # changing date of birth so user is underage
    request['date_of_birth'] = dt.date(1917, 5, 17)
    del request['state_of_birth']

    with pytest.raises(ValueError) as v:
        CurpValidationRequest(**request)
    assert 'state_of_birth required' in str(v)


def test_user_update_request():
    request = dict(
        beneficiaries=[
            dict(
                name='Pedro Pérez',
                birth_date=dt.date(2020, 1, 1),
                phone_number='+525555555555',
                user_relationship='brother',
                percentage=50,
            ),
            dict(
                name='José Pérez',
                birth_date=dt.date(2020, 1, 2),
                phone_number='+525544444444',
                user_relationship='brother',
                percentage=50,
            ),
        ],
        curp_document_uri='https://sandbox.cuenca.com/files/EF123',
    )
    update_req = UserUpdateRequest(**request)
    beneficiaries = [b.model_dump() for b in update_req.beneficiaries]
    assert beneficiaries == request['beneficiaries']
    assert (
        update_req.curp_document_uri.unicode_string()
        == request['curp_document_uri']
    )

    request['beneficiaries'] = [
        dict(
            name='Pedro Pérez',
            birth_date=dt.date(2020, 1, 1).isoformat(),
            phone_number='+525555555555',
            user_relationship='brother',
            percentage=50,
        ),
    ]
    assert UserUpdateRequest(**request)

    request['beneficiaries'] = [
        dict(
            name='Pedro Pérez',
            birth_date=dt.date(2020, 1, 1).isoformat(),
            phone_number='+525555555555',
            user_relationship='brother',
            percentage=101,
        ),
    ]
    with pytest.raises(ValueError) as v:
        UserUpdateRequest(**request)
        assert 'The total percentage is more than 100.' in str(v)

    tos_request = dict(
        terms_of_service=dict(
            version='2022-01-01',
            ip='127.0.0.1',
            location='1111,1111',
            type='ifpe',
        )
    )
    UserUpdateRequest(**tos_request)

    tos_request = dict(
        terms_of_service=dict(
            version='2022-01-01',
            ip='2001:0db8:0000:0000:0000:ff00:0042:8329',
            location='1111,1111',
            type='ifpe',
        )
    )
    UserUpdateRequest(**tos_request)

    kyc_request = dict(
        govt_id=dict(
            type='ine',
            uri_front='/files/FI-123',
            uri_back='/files/FI-456',
        )
    )
    UserUpdateRequest(**kyc_request)

    # chagning to invalid request
    tos_request['terms_of_service']['ip'] = 'not valid ip'
    with pytest.raises(ValueError) as v:
        UserUpdateRequest(**tos_request)
    assert 'not valid ip' in str(v.value)


def test_session_request():
    data = dict(
        user_id='sadsa', type=SessionType.registration, success_url='no url'
    )
    with pytest.raises(ValidationError):
        SessionRequest(**data)
    data['success_url'] = 'http://url.com'
    assert SessionRequest(**data)


def test_endpoint_request():
    data = dict(url='bad url', events=['user.create'])
    with pytest.raises(ValidationError):
        EndpointRequest(**data)
    data['url'] = 'http://url.com'
    assert EndpointRequest(**data)


def test_endpoint_update_request():
    data = dict(is_enable=True, events=['user.read'])
    with pytest.raises(ValidationError):
        EndpointUpdateRequest(**data)
    data['events'] = ['user.update']
    assert EndpointUpdateRequest(**data)


def test_email_verification_request():
    data = dict(
        recipient='mail@cuenca.com',
        type='email_verification',
        platform_id='PL01',
    )
    with pytest.raises(ValidationError):
        VerificationRequest(**data)
    data['type'] = 'email'
    assert VerificationRequest(**data)


def test_phone_verification_request():
    data = dict(
        recipient='+525555555555',
        type='phone_verification',
        platform_id='PL01',
    )
    with pytest.raises(ValidationError):
        VerificationRequest(**data)
    data['type'] = 'phone'
    assert VerificationRequest(**data)


def test_verification_attempt_request():
    assert VerificationAttemptRequest(**dict(code='111111'))


def test_limited_wallet_request():
    curp = 'TAXM840916HNEMXT02'
    rfc = 'TAXM840916123'
    # Not valid format
    with pytest.raises(ValidationError):
        LimitedWalletRequest(allowed_curp='123', allowed_rfc='123')

    assert LimitedWalletRequest(allowed_curp=curp, allowed_rfc=rfc)


def test_get_state_name():
    assert get_state_name(State.VZ) == 'Veracruz'


def test_bank_account_validation_clabe_request():
    assert BankAccountValidationRequest(account_number='646180157098510917')


@pytest.mark.parametrize(
    'input_data',
    [
        {'names': 'Pedro', 'first_surname': 'Paramo'},
        {'curp': 'GOCG650418HVZNML08'},
        {'rfc': 'GOCG650418TJ1'},
        {'account_number': '646180157034181180'},
        {
            'curp': 'GOCG650418HVZNML08',
            'rfc': 'GOCG650418TJ1',
            'names': 'Pedro',
            'first_surname': 'Paramo',
        },
    ],
)
def test_user_lists_request_valid_params(input_data):
    UserListsRequest(**input_data)


@pytest.mark.parametrize(
    'input_data,expected_error',
    [
        (
            {'first_surname': 'Paramo'},
            (
                'names is required when first_surname or second_surname '
                'is provided'
            ),
        ),
        (
            {'second_surname': 'Paramo'},
            (
                'names is required when first_surname or second_surname '
                'is provided'
            ),
        ),
        (
            {'first_surname': 'Paramo', 'second_surname': 'Paramo'},
            (
                'names is required when first_surname or second_surname '
                'is provided'
            ),
        ),
        (
            {'names': 'Juan'},
            'first_surname is required when names is provided',
        ),
        (
            {'first_surname': 'Paramo', 'curp': 'GOCG650418HVZNML08'},
            (
                'names is required when first_surname or second_surname '
                'is provided'
            ),
        ),
        ({}, 'At least 1 param is required'),
    ],
)
def test_user_lists_request_invalid_params(input_data, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        UserListsRequest(**input_data)


class IntModel(BaseModel):
    value: StrictPositiveInt


@pytest.mark.parametrize(
    "value, expected_error, expected_message",
    [
        (0, ValueError, "Input should be greater than 0"),
        (-5, ValueError, "Input should be greater than 0"),
        (
            21_474_836_48,
            ValueError,
            "Input should be less than or equal to 2147483647",
        ),
        (5.5, ValueError, "Input should be a valid integer"),
        ("10", ValueError, "Input should be a valid integer"),
    ],
)
def test_strict_positive_int_invalid(value, expected_error, expected_message):
    with pytest.raises(expected_error, match=expected_message):
        IntModel(value=value)


def validate_repeated_digits(password: str) -> str:
    """
    Example of a custom validator
    Check if the str contains repeated numbers
    """
    import re

    if re.search(r'(\d).*\1', password):
        raise ValueError("str cannot contain repeated digits")
    return password


class LogConfigModel(BaseModel):
    password: Annotated[Password, LogConfig(masked=True)]
    validated: Annotated[
        str, AfterValidator(validate_repeated_digits), LogConfig(masked=True)
    ]
    secret: Annotated[str, LogConfig(masked=True)]
    partial_secret: Annotated[
        str, LogConfig(masked=True, unmasked_chars_length=4)
    ]
    unmasked: Annotated[str, LogConfig(masked=False)]
    excluded: Annotated[str, LogConfig(excluded=True)]


@pytest.mark.parametrize(
    "field_name,expected_masked,expected_unmasked_length,expected_excluded",
    [
        ("password", True, 0, False),
        ("validated", True, 0, False),
        ("secret", True, 0, False),
        ("partial_secret", True, 4, False),
        ("unmasked", False, 0, False),
        ("excluded", False, 0, True),
    ],
)
def test_log_config(
    field_name, expected_masked, expected_unmasked_length, expected_excluded
):
    model = LogConfigModel(
        password="Mypass123.",
        validated="str123",
        secret="super-secret",
        partial_secret="1234567890",
        unmasked="unmasked",
        excluded="excluded",
    )

    field = model.model_fields[field_name]
    config = get_log_config(field)
    assert config.masked is expected_masked
    assert config.unmasked_chars_length == expected_unmasked_length
    assert config.excluded is expected_excluded


def test_get_log_config_no_log_config():
    field = FieldInfo(default=None)
    assert get_log_config(field) is None
