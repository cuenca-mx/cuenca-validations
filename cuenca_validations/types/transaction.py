import re

from enums import EntryType
from pydantic import BaseModel, validator

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
    commission={
        'Deposit': ['TR', 'SP', 'LT', 'CD'],
        'Transfer': ['TR', 'SP', 'LT'],
    },
)


class RelatedTransaction(str):
    def __init__(cls, uri: str):
        cls.uri = uri
        cls.id = cls._get_id(uri)
        cls.mapper_ids = cls._mapper_ids()

    @classmethod
    def __get_validators__(cls):
        yield cls
        yield cls.validate

    @classmethod
    def validate(cls, tr: 'Transaction') -> 'CallableGenerator':
        if tr.id[:2] not in tr.mapper_ids:
            raise ValueError('invalid id format')
        return tr

    @staticmethod
    def _get_id(uri: str) -> str:
        match = re.search(r'/[a-z]+/(\w+)', uri)
        return match.group(1)

    @staticmethod
    def _mapper_ids():
        return list(set(re.findall(r"'([A-Z]{0,2})'", str(mapper))))

    def get_model(cls, entry_type) -> str:
        if type(entry_type) is not EntryType:
            raise ValueError('The required enum is EntryType')
        return next(
            (
                model
                for model, types in mapper[entry_type.value].items()
                if cls.id[:2] in types
            ),
            None,
        )
