import pytest
from pydantic import ValidationError
from pydantic_extra_types.payment import PaymentCardBrand

from cuenca_validations.types import StrictPaymentCardNumber

VALID_BBVA = '4772130000000003'
INVALID_BIN = '4050000000000001'


def test_invalid_bin_strict_payment():
    with pytest.raises(ValidationError) as exc_info:
        card = StrictPaymentCardNumber(card_number=INVALID_BIN)
        print(card.card_number.bin)
    assert 'Invalid BIN: Bank code not found.' in str(exc_info.value)


def test_valid_bin_strict_payment():
    card = StrictPaymentCardNumber(card_number=VALID_BBVA)
    assert card.brand == PaymentCardBrand.visa
    assert card.bin == '477213'
    assert card.last4 == '0003'
    assert card.masked == '477213******0003'
    assert card.bank_code == '40012'
