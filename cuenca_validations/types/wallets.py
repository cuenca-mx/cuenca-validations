from typing import TYPE_CHECKING, ClassVar

from pydantic import ConstrainedStr
from pydantic.validators import (
    constr_length_validator,
    constr_strip_whitespace,
    str_validator,
)

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class WalletAccount(ConstrainedStr):
    account: str
    min_length: ClassVar[int] = 24
    max_length: ClassVar[int] = 24

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator': 
        yield cls