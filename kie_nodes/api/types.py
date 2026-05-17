from typing import Annotated

from pydantic import BeforeValidator

_coerce_to_list = BeforeValidator(lambda v: [v] if isinstance(v, str) else v)

ImageUrls = Annotated[list[str], _coerce_to_list]
VideoUrls = Annotated[list[str], _coerce_to_list]
AudioUrls = Annotated[list[str], _coerce_to_list]
