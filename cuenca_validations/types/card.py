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
                'payment_card_number.bin', 'Invalid BIN: Bank code not found.'
            )
        return card_number

    @property
    def brand(self) -> PaymentCardBrand:
        return self.number.brand

    @property
    def bank_code(self) -> str:
        return CARD_BINS.get(self.card_number.bin)
