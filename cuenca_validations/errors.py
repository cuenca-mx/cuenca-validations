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


class AuthedException(Exception):
    """Exceptions related to ApiKeys, Login, Password, etc"""


class NoPasswordFound(AuthedException):
    """User must create a password before to continue"""


class UserNotLoggedIn(AuthedException):
    """Login required for this method"""


class WrongCreds(AuthedException):
    """Invalid ApiKeys"""


class MissingAuthorizationHeader(AuthedException):
    """Neither Basic Auth or JWT found"""


class AuthMethodNotAllowed(AuthedException):
    """No permissions to use this authentication method"""


AUTHED_ERROR_CODES = {
    101: WrongCreds,
    102: MissingAuthorizationHeader,
    103: UserNotLoggedIn,
    104: NoPasswordFound,
    105: AuthMethodNotAllowed,
}
