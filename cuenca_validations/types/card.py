from typing import Annotated

from pydantic import Field, StringConstraints
from pydantic_core import PydanticCustomError, core_schema
from pydantic_extra_types.payment import PaymentCardNumber

from ..card_bins import CARD_BINS

ExpMonth = Annotated[int, Field(strict=True, ge=1, le=12)]
ExpYear = Annotated[int, Field(strict=True, ge=1, le=99)]
Cvv = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=3,
        pattern=r'\d{3}',
    ),
]


class StrictPaymentCardNumber(PaymentCardNumber):

    @classmethod
    def validate(
        cls, card_number: str, validation_info: core_schema.ValidationInfo
    ) -> 'StrictPaymentCardNumber':
        card = super().validate(card_number, validation_info)
        if card.bin not in CARD_BINS:
            raise PydanticCustomError(
                'payment_card_number.bin',
                'The card number contains a BIN (first six digits) that '
                'does not have a known association with a Mexican bank. '
                'To add the association, please file an issue: '
                'https://github.com/cuenca-mx/cuenca-validations/issues',
            )
        return cls(card)

    @property
    def bank_code(self) -> str:
        return CARD_BINS[self.bin]
