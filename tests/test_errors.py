from cuenca_validations.errors import (
    ApiError,
    AuthMethodNotAllowedError,
    CuencaError,
    InvalidOTPCodeError,
    MissingAuthorizationHeaderError,
    NoPasswordFoundError,
    TooManyAttemptsError,
    UserLocationError,
    UserNotLoggedInError,
    WrongCredsError,
)


def test_cuenca_error_base():
    assert issubclass(CuencaError, Exception)


def test_error_codes_and_status():
    test_cases = [
        (WrongCredsError, 101, 401),
        (MissingAuthorizationHeaderError, 102, 401),
        (UserNotLoggedInError, 103, 401),
        (NoPasswordFoundError, 104, 401),
        (AuthMethodNotAllowedError, 106, 401),
        (TooManyAttemptsError, 107, 403),
        (UserLocationError, 108, 401),
        (InvalidOTPCodeError, 109, 401),
        (ApiError, 500, 500),
    ]

    for error_class, expected_code, expected_status in test_cases:
        assert error_class.code == expected_code
        assert error_class.status_code == expected_status
