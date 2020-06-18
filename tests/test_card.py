import pytest
from pydantic import BaseModel
from pydantic.errors import PydanticValueError

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

    with pytest.raises(PydanticValueError):
        PaymentCard(card_number=INVALID_BIN)
