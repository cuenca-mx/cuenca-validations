import pytest

from cuenca_validations.validators import (
    normalize_email,
    normalize_name,
    normalize_phone_number,
)


@pytest.mark.parametrize(
    'raw, normalized',
    [
        ('user@Yahoo.com', 'user@yahoo.com'),  # uppercase domain
        ('user@iCloud.com', 'user@icloud.com'),  # uppercase domain
        ('user@Gmail.com', 'user@gmail.com'),  # uppercase domain
        ('user+cuenca@gmail.com', 'user@gmail.com'),  # plus label
        ('user@gmail.com', 'user@gmail.com'),  # already normalized
    ],
)
def test_normalize_email(raw: str, normalized: str) -> None:
    assert normalize_email(raw) == normalized


@pytest.mark.parametrize(
    'raw, normalized',
    [
        ('+116503456789', '+16503456789'),  # US duplicate country code
        ('+5215512345678', '+525512345678'),  # MX mobile prefix
        ('+520445512345678', '+525512345678'),  # MX 044 prefix
        ('+52 (55) 1234-5678', '+525512345678'),  # special characters
        ('+525512345678', '+525512345678'),  # already correct MX
        ('+16503456789', '+16503456789'),  # already correct US
    ],
)
def test_normalize_phone_number(raw: str, normalized: str) -> None:
    assert normalize_phone_number(raw) == normalized


@pytest.mark.parametrize(
    'raw, normalized',
    [
        ('Raúl Andrés', 'raul andres'),  # accents + mixed case
        ('raul andres', 'raul andres'),  # already normalized
        ('RAÚL ANDRÉS', 'raul andres'),  # uppercase with accents
        ('ÑANDÚ', 'nandu'),  # ñ and accent
        ('María  José', 'maria jose'),  # collapse internal whitespace
        ('  Raúl  ', 'raul'),  # trim + lowercase
        ('Nuño Garçía', 'nuno garcia'),  # tilde and cedilla
    ],
)
def test_normalize_name(raw: str, normalized: str) -> None:
    assert normalize_name(raw) == normalized
