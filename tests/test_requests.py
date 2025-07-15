from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude

from cuenca_validations.types.requests import (
    FileCuencaUrl,
    UserTOSAgreementRequest,
)


def test_file_cuenca_url() -> None:
    utos = UserTOSAgreementRequest(
        tos_id='TS67dcae8e74e81bba5a77bf47',
        location=Coordinate(Latitude('19.432607'), Longitude('-99.133209')),
        signature_image_url=FileCuencaUrl(
            'https://stage.cuenca.com/files/EFQL87ohvoRp-PkOTYgvQYFA'
        ),
    )
    assert utos.signature_image_url is not None
    assert utos.signature_image_url.file_id == 'EFQL87ohvoRp-PkOTYgvQYFA'
