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
    def validate_id(cls, v):
        ids = list(set(re.findall(r"'([A-Z]{0,2})'", str(mapper))))
        if v[:2] not in ids:
            raise ValueError('invalid id format')
        return v

    @validator('type')
    def validate_type(cls, v):
        if v not in mapper.keys():
            raise ValueError('invalid type format')
        return v

    def get_model(cls):
        for model, types in mapper[cls.type].items():
            if cls.id[:2] in types:
                return model
        return None
