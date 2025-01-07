from pydantic_core import PydanticCustomError, core_schema
from pydantic_extra_types.payment import PaymentCardNumber

from ..card_bins import CARD_BINS


class StrictPaymentCardNumber(PaymentCardNumber):
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

    @classmethod
    def validate(
        cls, __input_value: str, _: core_schema.ValidationInfo
    ) -> 'StrictPaymentCardNumber':
        card = super().validate(__input_value, _)
        if card.bin not in CARD_BINS:
            raise PydanticCustomError(
                'payment_card_number.bin',
                'The card number contains a BIN (first six digits) '
                'that does not have a known association with a Mexican bank.'
                'To add the association, please file an issue:'
                'https://github.com/cuenca-mx/cuenca-validations/issues',
            )
        return cls(card)

    @property
    def bank_code(self) -> str:
        return CARD_BINS[self.bin]
