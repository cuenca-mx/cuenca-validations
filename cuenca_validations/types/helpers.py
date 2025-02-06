import uuid
from base64 import urlsafe_b64encode
from typing import Callable, Optional

from pydantic.fields import FieldInfo

from .general import LogConfig


def uuid_field(prefix: str = '') -> Callable[[], str]:
    def base64_uuid_func() -> str:
        return prefix + urlsafe_b64encode(uuid.uuid4().bytes).decode()[:-2]

    return base64_uuid_func


def get_log_config(field: FieldInfo) -> Optional[LogConfig]:
    """Helper function to find LogConfig in field metadata"""
    try:
        return next(m for m in field.metadata if isinstance(m, LogConfig))
    except StopIteration:
        return None
