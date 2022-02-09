import datetime as dt
import json
from dataclasses import dataclass
from enum import Enum

import pytest
from freezegun import freeze_time
from pydantic import BaseModel, ValidationError

from cuenca_validations.types import (
    CardQuery,
    JSONEncoder,
    QueryParams,
    SantizedDict,
    TransactionStatus,
    digits,
)
from cuenca_validations.types.enums import Country, EcommerceIndicator, State
from cuenca_validations.types.requests import (
    ApiKeyUpdateRequest,
    ChargeRequest,
    CurpValidationRequest,
    SavingRequest,
    SavingUpdateRequest,
    UserCardNotificationRequest,
    UserCredentialUpdateRequest,
    UserRequest,
    UserUpdateRequest,
)

today = dt.date.today()
now = dt.datetime.now()
utcnow = now.astimezone(dt.timezone.utc)


class TestEnum(Enum):
    zero = 0


@dataclass
class TestClass:
    uno: str

    def to_dict(self):
        return dict(uno=self.uno, dos='dos')


def test_dict():
    model = QueryParams(count=1, created_before=now)
    assert model.dict() == dict(count=1, created_before=utcnow.isoformat())


def test_dict_with_exclude():
    model = QueryParams(count=1, created_before=now, user_id='USXXXX')
    assert model.dict(exclude={'user_id'}) == dict(
        count=1, created_before=utcnow.isoformat()
    )


def test_dict_with_exclude_unset():
    model = QueryParams(count=1, created_before=now)
    assert model.dict(exclude_unset=False) == dict(
        count=1, created_before=utcnow.isoformat(), page_size=100
    )


def test_sanitized_dict():
    assert SantizedDict(
        status=TransactionStatus.succeeded, time=now, hello='there'
    ) == dict(status='succeeded', time=utcnow.isoformat(), hello='there')


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
        (TestEnum.zero, 0),
        (today, today.isoformat()),
        (now, utcnow.isoformat()),
        (TestClass(uno='uno'), dict(uno='uno', dos='dos')),
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

    class ClassWithoutToDict:
        ...

    invalid_class = ClassWithoutToDict()
    with pytest.raises(TypeError):
        json.dumps(invalid_class, cls=JSONEncoder)


class Accounts(BaseModel):
    number: digits(5, 8)  # type: ignore


def test_only_digits():
    acc = Accounts(number='123456')
    assert acc.number == '123456'


@pytest.mark.parametrize(
    'number, error',
    [
        ('123', 'value_error.any_str.min_length'),
        ('1234567890', 'value_error.any_str.max_length'),
        ('no_123', 'value_error.digits'),
    ],
)
def test_invalid_digits(number, error):
    with pytest.raises(ValueError) as exception:
        Accounts(number=number)
    assert error in str(exception)


def test_card_query_exp_cvv_if_number_set():
    values = dict(number='123456', exp_month=1, exp_year=2026)
    card_query = CardQuery(**values)
    assert all(
        getattr(card_query, key) == value for key, value in values.items()
    )


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
    assert request.dict() == dict(user_id='US123')


def test_update_one_property_at_a_time_request():
    with pytest.raises(ValueError):
        UserCredentialUpdateRequest(user_id='US123', password='123456')

    req = UserCredentialUpdateRequest(password='123456')
    assert not req.is_active and req.password == '123456'

    req = UserCredentialUpdateRequest(is_active=True)
    assert req.is_active and not req.password


@pytest.mark.parametrize(
    'data,expected_dict',
    [
        (dict(password='123456'), dict(password='123456', is_active=None)),
        (dict(is_active=True), dict(password=None, is_active=True)),
        (dict(), dict(password=None, is_active=None)),
    ],
)
def test_update_credential_update_request_dict(data, expected_dict):
    req = UserCredentialUpdateRequest(**data)
    assert req.dict() == expected_dict


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


@freeze_time('2022-01-01')
def test_user_request():
    request = dict(
        curp='ABCD920604HDFSRN03',
        phone_number='+525555555555',
        email_address='email@email.com',
        profession='worker',
        address=dict(
            street='calle 1',
            ext_number='2',
            int_number='3',
            postal_code='09900',
            state=State.DF.value,
            country=Country.MX,
            city='Obrera',
        ),
    )
    assert UserRequest(**request).dict() == request


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
        assert '5 validation errors for CurpValidationRequest' in str(v)

    req_curp = CurpValidationRequest(**request)
    assert req_curp.dict() == request

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
                birth_date=dt.datetime(2020, 1, 1),
                phone_number='+525555555555',
                user_relationship='brother',
                percentage=50,
            ),
            dict(
                name='José Pérez',
                birth_date=dt.datetime(2020, 1, 2),
                phone_number='+525544444444',
                user_relationship='brother',
                percentage=50,
            ),
        ]
    )
    update_req = UserUpdateRequest(**request)
    beneficiaries = [b.dict() for b in update_req.beneficiaries]
    assert beneficiaries == request['beneficiaries']

    request['beneficiaries'] = [
        dict(
            name='Pedro Pérez',
            birth_date=dt.datetime(2020, 1, 1).isoformat(),
            phone_number='+525555555555',
            user_relationship='brother',
            percentage=50,
        ),
    ]

    with pytest.raises(ValueError) as v:
        UserUpdateRequest(**request)
        assert (
            'The total percentage of beneficiaries does not add 100.' in str(v)
        )
