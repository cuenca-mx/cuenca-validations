import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, validator
from pydantic.types import ConstrainedInt, PositiveInt

from ..typing import DictStrAny
from ..validators import sanitize_dict
from .enums import (
    CardFundingType,
    CardIssuer,
    CardStatus,
    CardType,
    TransferNetwork,
)

MAX_PAGE_SIZE = 100


class PageSize(ConstrainedInt):
    gt = 0
    le = MAX_PAGE_SIZE


class QueryParams(BaseModel):
    count: bool = False
    page_size: PageSize = PageSize(MAX_PAGE_SIZE)
    limit: Optional[PositiveInt] = None
    user_id: Optional[str] = None
    created_before: Optional[dt.datetime] = None
    created_after: Optional[dt.datetime] = None
    related_transaction: Optional[str] = None

    class Config:
        extra = Extra.forbid  # raise ValidationError if there are extra fields

    def dict(self, *args, **kwargs) -> DictStrAny:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_unset', True)
        d = super().dict(*args, **kwargs)
        if self.count:
            d['count'] = 1
        sanitize_dict(d)
        return d


class TransactionQuery(QueryParams):
    status: Optional[str] = None


class TransferQuery(TransactionQuery):
    account_number: Optional[str] = None
    idempotency_key: Optional[str] = None
    tracking_key: Optional[str] = None
    network: Optional[TransferNetwork] = None


class DepositQuery(TransactionQuery):
    tracking_key: Optional[str] = None
    network: Optional[TransferNetwork] = None


class BillPaymentQuery(TransactionQuery):
    account_number: Optional[str] = None


class CardTransactionQuery(TransactionQuery):
    card_uri: Optional[str] = None


class ApiKeyQuery(QueryParams):
    active: Optional[bool] = None


class CardQuery(QueryParams):
    number: Optional[str] = None
    exp_month: Optional[int] = None
    exp_year: Optional[int] = None
    cvv: Optional[str] = None
    cvv2: Optional[str] = None
    icvv: Optional[str] = None
    pin_block: Optional[str] = None
    issuer: Optional[CardIssuer] = None
    funding_type: Optional[CardFundingType] = None
    status: Optional[CardStatus] = None
    type: Optional[CardType] = None

    @validator('exp_month', 'exp_year', 'cvv2', 'cvv')
    def query_by_exp_cvv_if_number_set(cls, v, values):
        if not values['number']:
            raise ValueError('Number must be set to query by exp or cvv')
        return v


class StatementQuery(QueryParams):
    year: int
    month: int

    @validator('month')
    def validate_year_month(cls, month, values):
        year = values['year']
        month_now = dt.date.today().replace(day=1)
        month_set = dt.date(year, month, 1)
        if month_set >= month_now:
            raise ValueError(f'{year}-{month} is not a valid year-month pair')
        return month


class AccountQuery(QueryParams):
    account_number: Optional[str] = None


class BalanceEntryQuery(QueryParams):
    funding_instrument_uri: Optional[str] = None
