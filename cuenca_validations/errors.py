from pydantic.errors import PydanticValueError


class CardBinValidationError(PydanticValueError):
    code = 'payment_card_number.bin'
    msg_template = 'card number does not have a valid Mexican debit card BIN'
