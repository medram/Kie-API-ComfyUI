from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

AspectRatio = Literal[
    "1:1",
    "4:3",
    "3:4",
    "16:9",
    "9:16",
    "2:3",
    "3:2",
    "21:9",
]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="A text description of the image you want to generate.",
        max_length=3000,
    )
    image_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="URL(s) of the input image(s) for reference (Edit mode only).",
    )
    aspect_ratio: AspectRatio = Field(
        default="1:1",
        description="Width-height ratio of the image, determining its visual form.",
    )
    quality: Literal["basic", "high"] = Field(
        default="basic",
        description="Basic outputs 2K images, while High outputs 4K images.",
    )


class Seedream45Payload(BaseModel):
    model: str = "seedream/4.5-text-to-image"
    input: InputSchema


class KieSeedream45API(KieAPI):
    def node_name(self) -> str:
        return "KieSeedream45Node"

    def set_payload(self, payload: dict):
        valid_payload = Seedream45Payload(input=InputSchema(**payload))
        # Infer model from whether reference images are provided
        if valid_payload.input.image_urls:
            valid_payload.model = "seedream/4.5-edit"
        else:
            valid_payload.model = "seedream/4.5-text-to-image"
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
