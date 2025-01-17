__all__ = [
    'ApiError',
    'AuthMethodNotAllowedError',
    'CuencaError',
    'ERROR_CODES',
    'InvalidOTPCodeError',
    'MissingAuthorizationHeaderError',
    'NoPasswordFoundError',
    'TooManyAttemptsError',
    'UserLocationError',
    'UserNotLoggedInError',
    'WrongCredsError',
]


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


class UserLocationError(CuencaError):
    """User not in the same location from which they logged in."""

    code = 108
    status_code = 401


class InvalidOTPCodeError(CuencaError):
    """OTP sent is invalid."""

    code = 109
    status_code = 401


class ApiError(CuencaError):
    """Internal error"""

    code = 500
    status_code = 500


ERROR_CODES = {
    exc.code: exc
    for exc in [
        WrongCredsError,
        MissingAuthorizationHeaderError,
        UserNotLoggedInError,
        NoPasswordFoundError,
        AuthMethodNotAllowedError,
        TooManyAttemptsError,
        UserLocationError,
        InvalidOTPCodeError,
    ]
}
