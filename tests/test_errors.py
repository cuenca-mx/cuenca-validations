import pytest

from cuenca_validations.errors import (
    ERROR_CODES,
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


def test_error_messages():
    test_message = "Mensaje de prueba"

    for error_class in ERROR_CODES.values():
        with pytest.raises(error_class) as exc_info:
            raise error_class(test_message)
        assert str(exc_info.value) == test_message


def test_error_codes_mapping():
    for error_class in ERROR_CODES.values():
        assert ERROR_CODES[error_class.code] == error_class


def test_api_error():
    with pytest.raises(ApiError) as exc_info:
        raise ApiError("Error interno")
    assert str(exc_info.value) == "Error interno"
    assert exc_info.value.code == 500
    assert exc_info.value.status_code == 500
