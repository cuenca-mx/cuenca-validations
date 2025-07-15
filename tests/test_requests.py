import pytest
from pydantic import ValidationError

from cuenca_validations.types.requests import UserTOSAgreementRequest


@pytest.mark.parametrize('environment', ['stage', 'sandbox', 'api'])
def test_file_cuenca_url(environment: str) -> None:
    request_data = {
        'tos_id': 'TS67dcae8e74e81bba5a77bf47',
        'location': (19.432607, -99.133209),
        'signature_image_url': (
            f'https://{environment}.cuenca.com/files/EFQL87ohvoRp-PkOTYgvQYFA'
        ),
    }
    utos = UserTOSAgreementRequest.model_validate(request_data)
    assert utos.signature_image_url is not None
    assert utos.signature_image_url.file_id == 'EFQL87ohvoRp-PkOTYgvQYFA'


def test_file_cuenca_url_invalid() -> None:
    request_data = {
        'tos_id': 'TS67dcae8e74e81bba5a77bf47',
        'location': (19.432607, -99.133209),
        'signature_image_url': (
            'https://cuenca.com/files/EFQL87ohvoRp-PkOTYgvQYFA/invalid'
        ),
    }
    with pytest.raises(ValidationError):
        UserTOSAgreementRequest.model_validate(request_data)
