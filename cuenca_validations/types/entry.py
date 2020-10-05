import re

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
)


class EntryModel(BaseModel):
    id: str
    type: str

    @validator('id')
    def validate_id(cls, id):
        ids = list(set(re.findall(r"'([A-Z]{0,2})'", str(mapper))))
        if id[:2] not in ids:
            raise ValueError('invalid id format')
        return id

    @validator('type')
    def validate_type(cls, entry_type):
        if entry_type not in mapper.keys():
            raise ValueError('invalid entry_type format')
        return entry_type

    def get_model(cls):
        return next(
            (
                model
                for model, types in mapper[cls.type].items()
                if cls.id[:2] in types
            ),
            None,
        )
