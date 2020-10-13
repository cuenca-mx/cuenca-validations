import pytest
from pydantic import BaseModel, ValidationError

from cuenca_validations.types import (
    CommissionType,
    EntryType,
    RelatedTransaction,
    RelatedTransactionType,
)


class Model(BaseModel):
    related_transaction_uri: RelatedTransaction


def test_related_transaction():
    transaction_uri = '/deposits/SPXXX'
    model = Model(related_transaction_uri=transaction_uri)
    assert model.related_transaction_uri == transaction_uri
    assert (
        model.related_transaction_uri.get_model(EntryType.credit) == 'Deposit'
    )


def test_related_transaction_mapper_entry():
    transaction_uri = '/deposits/SPXXX'
    model = Model(related_transaction_uri=transaction_uri)
    assert model.related_transaction_uri == transaction_uri
    assert (
        model.related_transaction_uri.get_model(
            CommissionType.cash_deposit.value
        )
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
