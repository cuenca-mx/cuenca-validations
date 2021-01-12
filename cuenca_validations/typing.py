from typing import Any, Dict, List, MutableMapping, Optional, Union

ClientRequestParams = Union[
    None, bytes, MutableMapping[str, Union[str, List[str]]]
]
DictStrAny = Dict[str, Any]
OptionalDict = Optional[Dict[str, Union[int, str]]]
