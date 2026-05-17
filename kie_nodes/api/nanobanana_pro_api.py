from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

AspectRatio = Literal[
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
    "auto",
]


class InputSchema(BaseModel):
    prompt: str = Field(
        ..., description="Text prompt to guide the image generation.", max_length=20000
    )
    image_input: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        max_length=8,
        description="Input images to transform or use as reference (up to 8).",
    )
    aspect_ratio: AspectRatio = Field(
        default="1:1",
        description="Aspect ratio of the generated image.",
    )
    resolution: Literal["1K", "2K", "4K"] = Field(
        default="1K",
        description="Resolution of the generated image.",
    )
    output_format: Literal["png", "jpg"] = Field(
        default="png",
        description="Format of the output image.",
    )


class NanoBananaProPayload(BaseModel):
    model: str = "nano-banana-pro"
    input: InputSchema


class KieNanoBananaProAPI(KieAPI):
    def node_name(self) -> str:
        return "KieNanoBananaProNode"

    def set_payload(self, payload: dict):
        valid_payload = NanoBananaProPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
