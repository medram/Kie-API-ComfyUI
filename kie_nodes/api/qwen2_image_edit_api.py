from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

ImageSize = Literal["1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9", "21:9"]
OutputFormat = Literal["png", "jpeg"]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="The prompt to edit the image with.",
        max_length=5000,
    )
    image_url: ImageUrls = Field(
        ...,
        validation_alias="images",
        description="URL(s) of the reference image(s) to guide the edit.",
    )
    image_size: ImageSize = Field(
        default="16:9",
        description="Image ratio.",
    )
    output_format: OutputFormat = Field(
        default="png",
        description="Generate image format.",
    )
    seed: int = Field(
        default=0,
        description="The same seed and prompt produce the same image.",
    )


class Qwen2ImageEditPayload(BaseModel):
    model: str = "qwen2/image-edit"
    input: InputSchema


class KieQwen2ImageEditAPI(KieAPI):
    def node_name(self) -> str:
        return "KieQwen2ImageEditNode"

    def set_payload(self, payload: dict):
        valid_payload = Qwen2ImageEditPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
