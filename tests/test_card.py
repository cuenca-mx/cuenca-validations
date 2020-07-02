import pytest
from pydantic import BaseModel, ValidationError

from cuenca_validations.errors import CardBinValidationError
from cuenca_validations.types import PaymentCardNumber, StrictPaymentCardNumber

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
        card_number: StrictPaymentCardNumber

    with pytest.raises(ValidationError) as exc_info:
        PaymentCard(card_number=INVALID_BIN)
    assert exc_info.value.errors()[0] == dict(
        loc=('card_number',),
        type=f'value_error.{CardBinValidationError.code}',
        msg=CardBinValidationError.msg_template,
    )


def test_valid_bin_strict_payment():
    cn = StrictPaymentCardNumber.validate_bin(PaymentCardNumber(VALID_BBVA))
    assert cn == VALID_BBVA
