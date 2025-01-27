from typing import Optional

from pydantic import BaseModel

from .enums import KYCFileType
from .general import SerializableHttpUrl


class BatchFileMetadata(BaseModel):
    id: Optional[str] = None
    is_back: bool
    type: KYCFileType
    url: SerializableHttpUrl
