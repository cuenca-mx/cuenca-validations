from typing import Optional

from pydantic import BaseModel, HttpUrl

from .enums import KYCFileType


class BatchFileMetadata(BaseModel):
    id: Optional[str] = None
    is_back: bool
    type: KYCFileType
    url: HttpUrl
