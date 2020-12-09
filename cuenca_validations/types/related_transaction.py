import re
from typing import List, Optional

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

    def __init__(cls, uri: str):
        cls.uri = uri
        resource_data = cls._get_resource(uri)
        cls.resource = resource_data[0]
        cls.id = resource_data[1]

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
    def _get_resource(uri: str) -> List[Optional[str]]:
        match = re.search(r'/([a-z_]+)/([\w]+)', uri)
        if not match:
            return [None, None]
        return [match.group(1), match.group(2)]

    def get_model(cls):
        return mapper[cls.resource] if cls.resource in mapper else None
