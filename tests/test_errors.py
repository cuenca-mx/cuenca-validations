import pytest

from cuenca_validations.errors import (
    ApiError,
    AuthMethodNotAllowedError,
    InvalidOTPCodeError,
    MissingAuthorizationHeaderError,
    NoPasswordFoundError,
    TooManyAttemptsError,
    UserLocationError,
    UserNotLoggedInError,
    WrongCredsError,
)


@pytest.mark.parametrize(
    "error_class, expected_code, expected_status",
    [
        (WrongCredsError, 101, 401),
        (MissingAuthorizationHeaderError, 102, 401),
        (UserNotLoggedInError, 103, 401),
        (NoPasswordFoundError, 104, 401),
        (AuthMethodNotAllowedError, 106, 401),
        (TooManyAttemptsError, 107, 403),
        (UserLocationError, 108, 401),
        (InvalidOTPCodeError, 109, 401),
        (ApiError, 500, 500),
    ],
)
def test_error_codes_and_status(error_class, expected_code, expected_status):
    assert error_class.code == expected_code
    assert error_class.status_code == expected_status
