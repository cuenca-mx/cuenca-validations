import datetime as dt

from cuenca_validations.types import CardQuery, QueryParams, TransferQuery

today = dt.date.today()
now = dt.datetime.now()
utcnow = now.astimezone(dt.timezone.utc)


def test_dict():
    model = QueryParams(count=1, created_before=now)
    assert model.dict() == dict(count=1, created_before=utcnow.isoformat())


def test_dict_with_exclude():
    model = QueryParams(count=1, created_before=now, user_id='USXXXX')
    assert model.dict(exclude={'user_id'}) == dict(
        count=1, created_before=utcnow.isoformat()
    )


def test_dict_with_exclude_unset():
    model = QueryParams(count=1, created_before=now)
    assert model.dict(exclude_unset=False) == dict(
        count=1, created_before=utcnow.isoformat(), page_size=100
    )


def test_exclude_query_params_fields():
    query = CardQuery(number='123', count=True)
    query_dict = query.dict(exclude_query_params=True)
    assert query_dict == dict(number='123')
    assert all(f not in QueryParams.__fields__ for f in query_dict.keys())


def test_include_user_id_filter():
    query = TransferQuery(user_id='US123', account_number='123', count=True)
    query_dict = query.dict(exclude_query_params=True)
    assert query_dict == dict(user_id='US123', account_number='123')
    assert all(
        f not in QueryParams.__fields__
        for f in query_dict.keys()
        if f != 'user_id'
    )
