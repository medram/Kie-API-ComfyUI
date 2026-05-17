from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from .base import KieAPI

_coerce_to_str = BeforeValidator(
    lambda v: (v[0] if v else "") if isinstance(v, (list, tuple)) else v
)


class InputSchema(BaseModel):
    image: Annotated[str, _coerce_to_str] = Field(
        ...,
        description="URL of the image to upscale.",
    )


class CrispUpscalePayload(BaseModel):
    model: str = "recraft/crisp-upscale"
    input: InputSchema


class KieCrispUpscaleAPI(KieAPI):
    def node_name(self) -> str:
        return "KieCrispUpscaleNode"

    def set_payload(self, payload: dict):
        valid_payload = CrispUpscalePayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the upscaled image URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
