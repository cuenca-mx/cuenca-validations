import re
from typing import Optional, Tuple

mapper = dict(
    bill_payments='BillPayment',
    card_transactions='CardTransaction',
    commissions='Commission',
    deposits='Deposit',
    transfers='Transfer',
    whatsapp_transfers='WhatsappTransfer',
)


class RelatedTransaction(str):
    uri: str
    resource: Optional[str]
    id: Optional[str]

    def __init__(cls, uri: str):
        cls.uri = uri
        cls.resource, cls.id = cls._get_resource_data(uri)

    @classmethod
    def __get_validators__(cls):
        yield cls
        yield cls.validate

    @classmethod
    def validate(cls, tr: 'RelatedTransaction') -> 'RelatedTransaction':
        if not tr.resource:
            raise ValueError('invalid uri format')
        return tr

    @staticmethod
    def _get_resource_data(uri: str) -> Tuple[Optional[str], Optional[str]]:
        match = re.search(r'/([a-z_]+)/([\w]+)', uri)
        if not match:
            return (None, None)
        return (match.group(1), match.group(2))

    def get_model(cls):
        return mapper[cls.resource] if cls.resource in mapper else None
