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


class AuthError(Exception):
    """Exceptions related to ApiKeys, Login, Password, etc"""

    code: int
    status_code: int


class WrongCredsError(AuthError):
    """Invalid ApiKeys"""

    code = 101
    status_code = 401


class MissingAuthorizationHeaderError(AuthError):
    """Neither Basic Auth or JWT found"""

    code = 102
    status_code = 401


class UserNotLoggedInError(AuthError):
    """Login required for this method"""

    code = 103
    status_code = 401


class NoPasswordFoundError(AuthError):
    """User must create a password before to continue"""

    code = 104
    status_code = 401


class AuthMethodNotAllowedError(AuthError):
    """No permissions to use this authentication method"""

    code = 105
    status_code = 401


ERROR_CODES = {
    exc.code: exc
    for exc in [
        WrongCredsError,
        MissingAuthorizationHeaderError,
        UserNotLoggedInError,
        NoPasswordFoundError,
        AuthMethodNotAllowedError,
    ]
}
