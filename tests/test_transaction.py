import pytest
from pydantic import BaseModel, ValidationError

from cuenca_validations.types import (
    DepositNetwork,
    RelatedTransaction,
    TransactionType,
)


class Model(BaseModel):
    related_transaction_uri: RelatedTransaction


def test_related_transaction():
    transaction_uri = '/deposits/SPXXX'
    model = Model(related_transaction_uri=transaction_uri)
    assert model.related_transaction_uri == transaction_uri
    assert (
        model.related_transaction_uri.get_model(TransactionType.commission)
        == 'Deposit'
    )


def test_invalid_value_uri_related_transaction():
    transaction_uri = '/deposits/XXXXX'
    with pytest.raises(ValidationError) as exc_info:
        Model(related_transaction_uri=transaction_uri)
    assert exc_info.value.errors()[0] == dict(
        loc=('related_transaction_uri',),
        type='value_error',
        msg='invalid value format',
    )


def test_invalid_value_id_related_transaction():
    transaction_uri = 'XXXXX'
    with pytest.raises(ValidationError) as exc_info:
        Model(related_transaction_uri=transaction_uri)
    assert exc_info.value.errors()[0] == dict(
        loc=('related_transaction_uri',),
        type='value_error',
        msg='invalid value format',
    )


def test_invalid_type_related_transaction():
    transaction_uri = '/deposits/SPXXX'
    model = Model(related_transaction_uri=transaction_uri)
    assert model.related_transaction_uri == transaction_uri
    with pytest.raises(ValueError) as exc_info:
        assert not model.related_transaction_uri.get_model(DepositNetwork.cash)
    assert str(exc_info.value) == 'The required enum is TransactionType'
