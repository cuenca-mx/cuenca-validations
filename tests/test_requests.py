import pytest
from pydantic import ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumber

from cuenca_validations.types.enums import (
    Country,
    OperatorRole,
    OperatorStatus,
    SessionType,
    VerificationType,
)
from cuenca_validations.types.queries import OperatorQuery
from cuenca_validations.types.requests import (
    LegalPersonRequest,
    LegalPersonUpdateRequest,
    OperatorLoginRequest,
    OperatorLoginResponse,
    OperatorRequest,
    OperatorUpdateRequest,
    PasswordResetRequest,
    SessionMetadata,
    SessionRequest,
    UpdateTransferRequest,
    UserTOSAgreementRequest,
    UserUpdateRequest,
    VerificationRequest,
)
from cuenca_validations.typing import DictStrAny

LEGAL_REPRESENTATIVE: DictStrAny = {
    'names': 'Juan',
    'first_surname': 'Perez',
    'job': 'Director General',
    'phone_number': '+525512345678',
    'email_address': 'juan.perez@aceros.com',
    'address': {
        'street': 'Reforma',
        'ext_number': '265',
        'postal_code_id': 'PC2ygq9j2bS9-9tsuVawzErA',
    },
}

LEGAL_PERSON_REQUEST: DictStrAny = {
    'legal_name': 'Aceros del Norte SA de CV',
    'rfc': 'ADN850101ABC',
    'address': {
        'street': 'Reforma',
        'ext_number': '265',
        'postal_code_id': 'PC2ygq9j2bS9-9tsuVawzErA',
    },
    'legal_representatives': [LEGAL_REPRESENTATIVE],
}


def test_legal_person_request_valid() -> None:
    req = LegalPersonRequest.model_validate(LEGAL_PERSON_REQUEST)
    assert req.legal_name == 'Aceros del Norte SA de CV'
    assert req.rfc == 'ADN850101ABC'


def test_legal_person_request_rejects_physical_rfc() -> None:
    with pytest.raises(ValidationError) as ex:
        LegalPersonRequest.model_validate(
            {**LEGAL_PERSON_REQUEST, 'rfc': 'GOCG650418TJ1'}
        )
    assert 'RFC must be 12 characters for legal persons' in str(ex.value)


def test_legal_person_request_forbids_extra() -> None:
    with pytest.raises(ValidationError) as ex:
        LegalPersonRequest.model_validate(
            {**LEGAL_PERSON_REQUEST, 'foo': 'bar'}
        )
    assert 'Extra inputs are not permitted' in str(ex.value)


def test_legal_person_update_requires_at_least_one_param() -> None:
    with pytest.raises(ValueError) as ex:
        LegalPersonUpdateRequest()
    assert 'At least one parameter must be provided' in str(ex.value)


def test_legal_person_update_valid() -> None:
    req = LegalPersonUpdateRequest.model_validate({'legal_name': 'New name'})
    assert req.legal_name == 'New name'


def test_legal_person_update_accepts_legal_rfc() -> None:
    req = LegalPersonUpdateRequest.model_validate({'rfc': 'ADN850101ABC'})
    assert req.rfc == 'ADN850101ABC'


def test_legal_person_update_rejects_physical_rfc() -> None:
    with pytest.raises(ValidationError) as ex:
        LegalPersonUpdateRequest.model_validate({'rfc': 'GOCG650418TJ1'})
    assert 'RFC must be 12 characters for legal persons' in str(ex.value)


def test_operator_request_valid() -> None:
    req = OperatorRequest(
        name='Maria Lopez',
        email='Maria+Tag@Aceros.com',
        phone=PhoneNumber('+525512345678'),
        company_user_id='USWqY5cvkISJOxHyEKjAKf8w',
        role=OperatorRole.operator,
    )
    assert req.email == 'maria@aceros.com'
    assert req.status == OperatorStatus.active


def test_operator_request_rejects_invalid_role() -> None:
    with pytest.raises(ValidationError) as ex:
        OperatorRequest.model_validate(
            {
                'name': 'Maria Lopez',
                'email': 'maria@aceros.com',
                'phone': '+525512345678',
                'company_user_id': 'USWqY5cvkISJOxHyEKjAKf8w',
                'role': 'admin',
            }
        )
    assert 'role' in str(ex.value)


def test_operator_update_requires_at_least_one_param() -> None:
    with pytest.raises(ValueError) as ex:
        OperatorUpdateRequest()
    assert 'At least one parameter must be provided' in str(ex.value)


def test_operator_update_valid() -> None:
    req = OperatorUpdateRequest.model_validate({'name': 'New name'})
    assert req.name == 'New name'


def test_operator_login_request_valid() -> None:
    req = OperatorLoginRequest.model_validate(
        {
            'email': 'Operator+Tag@Aceros.com',
            'password': 'supersecret',
        }
    )
    assert req.email == 'operator@aceros.com'


def test_operator_login_request_rejects_short_password() -> None:
    with pytest.raises(ValidationError) as ex:
        OperatorLoginRequest.model_validate(
            {
                'email': 'operator@aceros.com',
                'password': 'short',
            }
        )
    assert 'password' in str(ex.value)


def test_operator_login_request_forbids_extra() -> None:
    with pytest.raises(ValidationError) as ex:
        OperatorLoginRequest.model_validate(
            {
                'email': 'operator@aceros.com',
                'password': 'supersecret',
                'foo': 'bar',
            }
        )
    assert 'Extra inputs are not permitted' in str(ex.value)


def test_operator_login_response_valid() -> None:
    resp = OperatorLoginResponse(session_token='SEWqY5cvkISJOxHyEKjAKf8w')
    assert resp.session_token == 'SEWqY5cvkISJOxHyEKjAKf8w'


def test_operator_query_valid() -> None:
    query = OperatorQuery.model_validate({'email': 'maria.lopez@aceros.com'})
    assert str(query.email) == 'maria.lopez@aceros.com'


def test_operator_query_forbids_extra() -> None:
    with pytest.raises(ValidationError) as ex:
        OperatorQuery.model_validate(
            {'email': 'maria@aceros.com', 'foo': 'bar'}
        )
    assert 'Extra inputs are not permitted' in str(ex.value)


def test_session_request_with_operator_metadata() -> None:
    req = SessionRequest(
        user_id='USWqY5cvkISJOxHyEKjAKf8w',
        type=SessionType.registration,
        metadata=SessionMetadata(operator_id='OPWqY5cvkISJOxHyEKjAKf8w'),
    )
    assert req.metadata is not None
    assert req.metadata.operator_id == 'OPWqY5cvkISJOxHyEKjAKf8w'


def test_session_request_metadata_forbids_extra() -> None:
    with pytest.raises(ValidationError) as ex:
        SessionMetadata.model_validate(
            {'operator_id': 'OPWqY5cvkISJOxHyEKjAKf8w', 'foo': 'bar'}
        )
    assert 'Extra inputs are not permitted' in str(ex.value)


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


def test_password_reset_request_serializes() -> None:
    payload: DictStrAny = {'location': (19.432607, -99.133209)}
    req = PasswordResetRequest.model_validate(payload)
    assert req.model_dump() == {
        'location': {
            'latitude': 19.432607,
            'longitude': -99.133209,
        },
    }


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


def test_verification_request_normalizes_email() -> None:
    req = VerificationRequest(
        recipient='user+cuenca@Gmail.com',
        type=VerificationType.email,
    )
    assert req.recipient == 'user@gmail.com'


def test_verification_request_normalizes_phone() -> None:
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


def test_user_update_request_accepts_country_of_birth() -> None:
    req = UserUpdateRequest(country_of_birth=Country.CA)
    assert req.country_of_birth == Country.CA


@pytest.mark.parametrize('status', ['succeeded', 'failed'])
def test_update_transfer_request_valid_status(status: str) -> None:
    req = UpdateTransferRequest.model_validate({'status': status})
    assert req.status == status
    assert req.model_dump() == {'status': status}


@pytest.mark.parametrize('status', ['created', 'submitted', 'in_review'])
def test_update_transfer_request_invalid_status(status: str) -> None:
    with pytest.raises(ValidationError) as ex:
        UpdateTransferRequest.model_validate({'status': status})
    assert 'status' in str(ex.value)


def test_update_transfer_request_missing_status() -> None:
    with pytest.raises(ValidationError) as ex:
        UpdateTransferRequest.model_validate({})
    assert 'status' in str(ex.value)


def test_update_transfer_request_forbids_extra() -> None:
    with pytest.raises(ValidationError) as ex:
        UpdateTransferRequest.model_validate(
            {'status': 'succeeded', 'foo': 'bar'}
        )
    assert 'Extra inputs are not permitted' in str(ex.value)
