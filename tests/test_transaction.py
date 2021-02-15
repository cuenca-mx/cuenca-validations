import pytest
from pydantic import BaseModel, ValidationError

from cuenca_validations.types import RelatedResource


class Model(BaseModel):
    related_uri: RelatedResource


def test_related_account():
    transaction_uri = '/accounts/BAXXX'
    model = Model(related_uri=transaction_uri)
    assert model.related_uri == transaction_uri
    assert model.related_uri.get_model() == 'Account'
    assert model.related_uri.id == 'BAXXX'


def test_related_transaction():
    transaction_uri = '/deposits/SPXXX'
    model = Model(related_uri=transaction_uri)
    assert model.related_uri == transaction_uri
    assert model.related_uri.get_model() == 'Deposit'
    assert model.related_uri.id == 'SPXXX'


def test_related_transaction_with_underscore():
    transaction_uri = '/bill_payments/STXXX'
    model = Model(related_uri=transaction_uri)
    assert model.related_uri == transaction_uri
    assert model.related_uri.get_model() == 'BillPayment'
    assert model.related_uri.id == 'STXXX'


def test_invalid_uri_related_transaction():
    transaction_uri = '/depositsXXXXX'
    with pytest.raises(ValidationError) as exc_info:
        Model(related_uri=transaction_uri)
    assert exc_info.value.errors()[0] == dict(
        loc=('related_uri',),
        type='value_error',
        msg='invalid uri format',
    )
