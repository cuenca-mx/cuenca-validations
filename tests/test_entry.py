import pytest
from pydantic import ValidationError

from cuenca_validations.types import EntryModel


def test_entry_model():
    entry = EntryModel(id='SPXXX', type='credit')
    assert entry.get_model() == 'Deposit'


def test_entry_model_none_for_type_incorrect():
    entry = EntryModel(id='CDXXX', type='debit')
    assert not entry.get_model()


def test_invalid_id_entry_model():
    with pytest.raises(ValidationError) as exc_info:
        EntryModel(id='XXXXX', type='credit')
    assert exc_info.value.errors()[0] == dict(
        loc=('id',),
        type='value_error',
        msg='invalid id format',
    )


def test_invalid_type_entry_model():
    with pytest.raises(ValidationError) as exc_info:
        EntryModel(id='SPXXX', type='foo')
    assert exc_info.value.errors()[0] == dict(
        loc=('type',),
        type='value_error',
        msg='invalid type format',
    )
