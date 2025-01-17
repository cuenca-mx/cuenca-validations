from typing import Any, MutableMapping, Optional, Union

ClientRequestParams = Union[None, bytes, MutableMapping[str, str]]
DictStrAny = dict[str, Any]
OptionalDict = Optional[dict[str, Union[int, str]]]
