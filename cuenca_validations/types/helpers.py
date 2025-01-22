import uuid
from base64 import urlsafe_b64encode
from typing import Callable


def uuid_field(prefix: str = '') -> Callable[[], str]:
    def base64_uuid_func() -> str:
        return prefix + urlsafe_b64encode(uuid.uuid4().bytes).decode()[:-2]

    return base64_uuid_func
