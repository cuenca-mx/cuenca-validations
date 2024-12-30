from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from pydantic_extra_types.payment import PaymentCardBrand, PaymentCardNumber

from ..card_bins import CARD_BINS


class StrictPaymentCardNumber(BaseModel):

    card_number: PaymentCardNumber

    @field_validator('card_number')
    def validate_bin(cls, card_number: PaymentCardNumber) -> PaymentCardNumber:
        if card_number.bin not in CARD_BINS:
            raise PydanticCustomError(
                'payment_card_number.bin',
                'The card number contains a BIN (first six digits) '
                'that does not have a known association with a Mexican bank.'
                'To add the association, please file an issue:'
                'https://github.com/cuenca-mx/cuenca-validations/issues',
            )
        return card_number

    @property
    def brand(self) -> PaymentCardBrand:
        return self.card_number.brand

    @property
    def last4(self) -> str:
        return self.card_number.last4

    @property
    def masked(self) -> str:
        return self.card_number.masked

    @property
    def bin(self) -> str:
        return self.card_number.bin

    @property
    def bank_code(self) -> str:
        return CARD_BINS[self.card_number.bin]
