import pytest
from pydantic import BaseModel, ValidationError
from pydantic_extra_types.payment import PaymentCardBrand

from cuenca_validations.types import StrictPaymentCardNumber

VALID_BBVA = '4772130000000003'
INVALID_BIN = '4050000000000001'


class CardModel(BaseModel):
    card_number: StrictPaymentCardNumber


def test_invalid_bin_strict_payment():
    with pytest.raises(ValidationError) as exc_info:
        CardModel(card_number=INVALID_BIN)
    print(exc_info.value)
    assert 'payment_card_number.bin' in str(exc_info.value)
    assert 'The card number contains a BIN (first six digits) ' in str(
        exc_info.value
    )


def test_valid_bin_strict_payment():
    card = CardModel(card_number=VALID_BBVA)
    assert card.card_number.brand == PaymentCardBrand.visa
    assert card.card_number.bin == '477213'
    assert card.card_number.last4 == '0003'
    assert card.card_number.masked == '477213******0003'
    assert card.card_number.bank_code == '40012'
