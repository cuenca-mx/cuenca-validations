import re
from typing import Optional

from .enums import EntryType

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
    id: Optional[str]
    uri: str
    mapper_ids: list

    def __init__(cls, uri: str):
        cls.uri = uri
        cls.id = cls._get_id(uri)
        cls.mapper_ids = cls._mapper_ids()

    @classmethod
    def __get_validators__(cls):
        yield cls
        yield cls.validate

    @classmethod
    def validate(cls, tr: 'RelatedTransaction') -> 'RelatedTransaction':
        if not tr.id:
            raise ValueError('invalid uri format')
        if tr.id[:2] not in tr.mapper_ids:
            raise ValueError('invalid id format')
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

    def get_model(cls, entry_type: EntryType):
        return next(
            (
                model
                for model, types in mapper[entry_type.value].items()
                if cls.id and cls.id[:2] in types
            ),
            None,
        )
