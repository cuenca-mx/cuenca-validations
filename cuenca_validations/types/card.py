from typing import TYPE_CHECKING, ClassVar

from pydantic.types import PaymentCardNumber as PydanticPaymentCardNumber
from pydantic.validators import (
    constr_length_validator,
    constr_strip_whitespace,
    str_validator,
)

from ..card_bins import CARD_BINS
from ..errors import CardBinValidationError

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class PaymentCardNumber(PydanticPaymentCardNumber):
    min_length: ClassVar[int] = 16
    max_length: ClassVar[int] = 16

    def __init__(self, card_number: str):
        self.bin = card_number[:6]
        self.last4 = card_number[-4:]
        self.brand = self._get_brand(card_number)
        self.bank_code = CARD_BINS.get(self.bin)

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield str_validator
        yield constr_strip_whitespace
        yield constr_length_validator
        yield cls.validate_digits
        yield cls.validate_luhn_check_digit
        yield cls


class StrictPayemntCardNumber(PaymentCardNumber):
    """
    requires that the BIN be associated to a known BIN for a Mexican bank
    """

    def __init__(self, card_number: str):
        self.card_number = card_number
        PaymentCardNumber.__init__(self, card_number)

    def validate_bin(self):
        if self.bank_code is None:
            raise CardBinValidationError
        return self.card_number
