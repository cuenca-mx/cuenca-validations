.. cuenca-validations documentation master file, created by
   sphinx-quickstart on Tue Jun 16 14:21:22 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cuenca-validations
------------------

Cuenca-validations is a shared library across multiple projects and
allows you to validate data using pydantic. You can:

* Validate parameters for generate a query
* Validate the parameters for create an object of type Transfer.

Installation
---------------

Install the latest cuenca-validations release via pip:
::

      $ pip install cuenca-validatons

You may also install a specific version:
::

      $ pip install cuenca-validations==0.0.2


Using cuenca-validations
------------------------
To use cuenca-validations for validating the parameters that are received.
In the case that you want this for generating a query, you can use
QueryParams() and tell it what parameters you are going to use:

:count: Boolean (default: False)
:limit: Int (optional)
:user: String (optional)
:created_before: Datetime (optional)
:created_after: Datetime (optional)

::

      import datetime as dt
      from cuenca_validations.validators import QueryParams


      # Let's filter by one date, using the
      # parameters count and created_before

      now = dt.datetime.utcnow()
      model = QueryParams(count=1, created_before=now)

You can limit the return results, the maximum limit is 100.
Note, use the parameters for a best performance in the query.

If you want to validate the received parameters of a transfer,
you can use TransferRequest() and the following parameters:

:recipient_name: StrictStr
:account_number: Union[Clabe, PaymentCardNumber]
:amount: StrictPositiveInt  # in centavos
:descriptor: StrictStr  # how it'll appear for the recipient
:created_after: String  # must be unique for each transfer

::

      from cuenca_validations.validators import TransferRequest
      .
      .
      TransferRequest(**transfer)
