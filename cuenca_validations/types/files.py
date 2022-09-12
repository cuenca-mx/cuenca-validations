from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from .enums import KYCFileType, ServiceProviderFieldType


class BatchFileMetadata(BaseModel):
    id: Optional[str]
    is_back: bool
    type: KYCFileType
    url: HttpUrl


class ServiceProviderField(BaseModel):
    is_active: bool
    requires_accountholder_name: bool
    mask: str
    topup_amounts: List[int]
    type: ServiceProviderFieldType
