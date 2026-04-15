import pytest
from pydantic import ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumber

from cuenca_validations.types.enums import VerificationType
from cuenca_validations.types.requests import (
    UserTOSAgreementRequest,
    UserUpdateRequest,
    VerificationRequest,
)
from cuenca_validations.typing import DictStrAny


@pytest.mark.parametrize('environment', ['api.stage', 'api.sandbox', 'api'])
def test_file_cuenca_url(environment: str) -> None:
    request_data: DictStrAny = dict(
        tos_id='TS67dcae8e74e81bba5a77bf47',
        location=(19.432607, -99.133209),
        signature_image_url=(
            f'https://{environment}.cuenca.com/files/EFQL8_ohvoRp-PkOTYgvQYFA'
        ),
    )
    utos = UserTOSAgreementRequest(**request_data)
    assert utos.signature_image_url is not None
    assert utos.signature_image_url.file_id == 'EFQL8_ohvoRp-PkOTYgvQYFA'


def test_file_cuenca_url_invalid() -> None:
    request_data: DictStrAny = dict(
        tos_id='TS67dcae8e74e81bba5a77bf47',
        location=(19.432607, -99.133209),
        signature_image_url=(
            'https://cuenca.com/files/EFQL87ohvoRp-PkOTYgvQYFA/invalid'
        ),
    )
    with pytest.raises(ValidationError):
        UserTOSAgreementRequest(**request_data)


def test_update_user_requires_at_least_one_param():
    with pytest.raises(ValueError) as ex:
        UserUpdateRequest()
    assert 'At least one parameter must be provided' in str(ex.value)


def test_extra_params_are_not_allowed():
    with pytest.raises(ValueError) as ex:
        UserUpdateRequest(foo='bar')
    assert 'Extra inputs are not permitted' in str(ex.value)


def test_update_user_update_govt() -> None:
    govt_id: DictStrAny = {
        "govt_id": {"type": "ine", "uri_front": "files/123"}
    }
    with pytest.raises(ValueError) as ex:
        UserUpdateRequest(**govt_id)
    assert 'uri_back must be provided for type ine' in str(ex.value)


def test_update_user_normalizes_email() -> None:
    req = VerificationRequest(
        recipient='user+cuenca@Gmail.com',
        type=VerificationType.email,
    )
    assert req.recipient == 'user@gmail.com'


def test_update_user_normalizes_phone() -> None:
    req = VerificationRequest(
        recipient='+116504401222',
        type=VerificationType.phone,
    )
    assert req.recipient == '+16504401222'


def test_user_update_request_normalizes_email() -> None:
    req = UserUpdateRequest(email_address='user+tag@Gmail.com')
    assert req.email_address == 'user@gmail.com'


def test_user_update_request_normalizes_phone() -> None:
    req = UserUpdateRequest(phone_number=PhoneNumber('+116504401222'))
    assert req.phone_number == '+16504401222'
