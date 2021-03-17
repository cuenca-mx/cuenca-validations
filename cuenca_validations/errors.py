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


class CuencaError(Exception):
    """Exceptions related to ApiKeys, Login, Password, etc"""

    code: int
    status_code: int


class WrongCredsError(CuencaError):
    """Invalid ApiKeys"""

    code = 101
    status_code = 401


class MissingAuthorizationHeaderError(CuencaError):
    """Neither Basic Auth or JWT found"""

    code = 102
    status_code = 401


class UserNotLoggedInError(CuencaError):
    """Login required for this method"""

    code = 103
    status_code = 401


class NoPasswordFoundError(CuencaError):
    """User must create a password before to continue"""

    code = 104
    status_code = 401


class AuthMethodNotAllowedError(CuencaError):
    """No permissions to use this authentication method"""

    code = 106
    status_code = 401


class TooManyAttemptsError(CuencaError):
    """This user has tried too many times to activate a card"""

    code = 107
    status_code = 403


ERROR_CODES = {
    exc.code: exc
    for exc in [
        WrongCredsError,
        MissingAuthorizationHeaderError,
        UserNotLoggedInError,
        NoPasswordFoundError,
        AuthMethodNotAllowedError,
        TooManyAttemptsError,
    ]
}
