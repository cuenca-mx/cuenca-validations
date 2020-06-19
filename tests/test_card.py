import pytest
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from cuenca_validations import PaymentCardNumber, StrictPayemntCardNumber

VALID_BBVA = '4772130000000003'
INVALID_BIN = '4050000000000001'


def test_valid_bin():
    class PaymentCard(BaseModel):
        card_number: PaymentCardNumber

    pc = PaymentCard(card_number=VALID_BBVA)
    assert pc.card_number.bin == '477213'
    assert pc.card_number.bank_code == '40012'


def test_invalid_bin():
    class PaymentCard(BaseModel):
        card_number: StrictPayemntCardNumber

    with pytest.raises(ValidationError) as exc_info:
        PaymentCard(card_number=INVALID_BIN)
    assert exc_info.value.errors() == [
        {
            'loc': ('card_number',),
            'msg': 'card number does not have a valid Mexican debit card BIN',
            'type': 'value_error.payment_card_number.bin',
        }
    ]


def test_valid_bin_strict_payment():
    cn = StrictPayemntCardNumber.validate_bin(PaymentCardNumber(VALID_BBVA))
    assert cn == VALID_BBVA
