import re
from typing import Optional

from .enums import CommissionType, EntryType

mapper = dict(
    credit={
        'Deposit': ['TR', 'SP', 'LT', 'CD'],
        'CardTransaction': ['CT'],
    },
    debit={
        'BillPayment': ['ST'],
        'Transfer': ['TR', 'SP', 'LT'],
        'WhatsappTransfer': ['SW'],
        'Commission': ['CO'],
        'CardTransaction': ['CT'],
    },
)


class RelatedTransaction(str):
    id: str
    uri: str
    mapper_ids: list

    def __init__(cls, value: str):
        cls.uri = value
        cls.id = cls._get_id(value) or value
        cls.mapper_ids = cls._mapper_ids()

    @classmethod
    def __get_validators__(cls):
        yield cls
        yield cls.validate

    @classmethod
    def validate(cls, tr: 'RelatedTransaction') -> 'RelatedTransaction':
        if not tr.id or tr.id[:2] not in tr.mapper_ids:
            raise ValueError('invalid value format')
        return tr

    @staticmethod
    def _get_id(uri: str) -> Optional[str]:
        match = re.search(r'/[a-z]+/(\w+)', uri)
        if not match:
            return None
        return match.group(1)

    @staticmethod
    def _mapper_ids():
        return list(set(re.findall(r"'([A-Z]{0,2})'", str(mapper))))

    def get_model(cls, _type: str):
        return next(
            (
                model
                for model, types in mapper[_type].items()
                if cls.id[:2] in types
            ),
            None,
        )
