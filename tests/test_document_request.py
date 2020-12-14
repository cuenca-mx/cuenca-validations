from datetime import date

import pytest
from pydantic import ValidationError

from cuenca_validations.types import DocumentRequest, DocumentType


def test_valid_document_request():
    document = DocumentRequest(
        client_name='Iron Man',
        clabe='002000000000000008',
        address='Address Foo',
        rfc='GODE561231GR8',
        date=(2020, 11),
        document_type=DocumentType.invoice,
    )
    assert document.client_name == 'Iron Man'
    assert document.date == date(2020, 11, 1)
    assert document.document_type == DocumentType.invoice


def test_invalid_rfc_document_request():
    with pytest.raises(ValidationError) as exc_info:
        DocumentRequest(
            client_name='Iron Man',
            clabe='002000000000000008',
            address='Address Foo',
            rfc='fooo',
            date=(2020, 11),
            document_type=DocumentType.invoice,
        )
    assert exc_info.value.errors()[0] == dict(
        loc=('rfc',),
        type='value_error',
        msg='Invalid rfc format',
    )


def test_invalid_date_document_request():
    now = date.today()
    with pytest.raises(ValidationError) as exc_info:
        DocumentRequest(
            client_name='Iron Man',
            clabe='002000000000000008',
            address='Address Foo',
            rfc='GODE561231GR8',
            date=(now.year, now.month),
            document_type=DocumentType.invoice,
        )
    assert exc_info.value.errors()[0] == dict(
        loc=('date',),
        type='value_error',
        msg='You cannot check the current month',
    )
