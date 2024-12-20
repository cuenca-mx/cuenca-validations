from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

from .enums import KYCFileType


class BatchFileMetadata(BaseModel):
    id: Optional[str] = None
    is_back: bool
    type: KYCFileType
    url: AnyHttpUrl
