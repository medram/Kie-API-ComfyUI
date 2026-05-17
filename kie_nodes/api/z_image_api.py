from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

AspectRatio = Literal["1:1", "4:3", "3:4", "16:9", "9:16"]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="Text description of the image to generate.",
        max_length=1000,
    )
    aspect_ratio: AspectRatio = Field(
        default="1:1",
        description="Aspect ratio of the generated image.",
    )


class ZImagePayload(BaseModel):
    model: str = "z-image"
    input: InputSchema


class KieZImageAPI(KieAPI):
    def node_name(self) -> str:
        return "KieZImageNode"

    def set_payload(self, payload: dict):
        valid_payload = ZImagePayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
