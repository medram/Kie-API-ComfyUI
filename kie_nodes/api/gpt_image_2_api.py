from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

AspectRatio = Literal[
    "auto",
    "1:1",
    "5:4",
    "9:16",
    "21:9",
    "16:9",
    "4:3",
    "3:2",
    "4:5",
    "3:4",
    "2:3",
]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="Used to describe the generated images.",
        max_length=20000,
    )
    input_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="URL(s) of the input image(s) for reference (I2I only).",
        max_length=14,
    )
    aspect_ratio: AspectRatio = Field(
        default="auto",
        description="The aspect ratio of the generated image.",
    )
    resolution: Literal["1K", "2K", "4K"] = Field(
        default="1K",
        description="Image resolution. Note: 1:1 aspect ratio cannot use 4K; 'auto' aspect ratio only supports 1K.",
    )


class GptImage2Payload(BaseModel):
    model: str = "gpt-image-2-text-to-image"
    input: InputSchema


class KieGptImage2API(KieAPI):
    def node_name(self) -> str:
        return "KieGptImage2Node"

    def set_payload(self, payload: dict):
        valid_payload = GptImage2Payload(input=InputSchema(**payload))
        # Infer model from whether reference images are provided
        if valid_payload.input.input_urls:
            valid_payload.model = "gpt-image-2-image-to-image"
        else:
            valid_payload.model = "gpt-image-2-text-to-image"
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
