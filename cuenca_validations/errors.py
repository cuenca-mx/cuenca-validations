__all__ = ['CardBinValidationError', 'NotDigitError']

from pydantic.errors import (
    NotDigitError as PydanticNotDigitError,
    PydanticValueError,
)


class CardBinValidationError(PydanticValueError):
    code = 'payment_card_number.bin'
    msg_template = (
        'The card number contains a BIN (first six digits) that does not have'
        'a known association with a Mexican bank. To add the association,'
        'please file an issue:'
        'https://github.com/cuenca-mx/cuenca-validations/issues'
    )


class NotDigitError(PydanticNotDigitError):
    code = 'digits'
    msg_template = 'value is not all digits'
