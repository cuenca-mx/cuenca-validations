import pytest
from pydantic import BaseModel, ValidationError

from cuenca_validations.types import RelatedTransaction


class Model(BaseModel):
    related_transaction_uri: RelatedTransaction


def test_related_transaction():
    transaction_uri = '/deposits/SPXXX'
    model = Model(related_transaction_uri=transaction_uri)
    assert model.related_transaction_uri == transaction_uri
    assert model.related_transaction_uri.get_model() == 'Deposit'
    assert model.related_transaction_uri.id == 'SPXXX'


def test_related_transaction_with_underscore():
    transaction_uri = '/bill_payments/STXXX'
    model = Model(related_transaction_uri=transaction_uri)
    assert model.related_transaction_uri == transaction_uri
    assert model.related_transaction_uri.get_model() == 'BillPayment'
    assert model.related_transaction_uri.id == 'STXXX'


def test_invalid_uri_related_transaction():
    transaction_uri = '/depositsXXXXX'
    with pytest.raises(ValidationError) as exc_info:
        Model(related_transaction_uri=transaction_uri)
    assert exc_info.value.errors()[0] == dict(
        loc=('related_transaction_uri',),
        type='value_error',
        msg='invalid uri format',
    )
