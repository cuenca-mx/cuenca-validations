from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from pydantic_extra_types.payment import PaymentCardBrand, PaymentCardNumber

from ..card_bins import CARD_BINS


class StrictPaymentCardNumber(BaseModel):
    """
    Refactored `StrictPaymentCardNumber` to leverage Pydantic v2's
    `PaymentCardNumber`, which now natively includes attributes such as
    brand, bin, last4, and masked.

    Previously, these attributes were manually computed in a custom
    `PaymentCardNumber` class.

    The `StrictPaymentCardNumber` class now wraps `PaymentCardNumber`
    as a field, with additional validation to ensure the BIN is associated
    with a known Mexican bank.
    """

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
