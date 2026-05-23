from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

AspectRatio = Literal[
    "2:3",
    "3:2",
    "1:1",
    "16:9",
    "9:16",
]

Mode = Literal["fun", "normal", "spicy"]

Resolution = Literal["480p", "720p"]


class InputSchema(BaseModel):
    prompt: str = Field(
        default="",
        description="The text prompt describing the desired video motion.",
        max_length=5000,
    )
    image_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description=(
            "URL of the reference image for video generation (only one image is "
            "supported)."
        ),
    )
    mode: Mode = Field(
        default="normal",
        description=(
            "Generation mode. Spicy mode is not supported with external image "
            "inputs and will automatically switch to Normal."
        ),
    )
    aspect_ratio: AspectRatio = Field(
        default="2:3",
        description="Aspect ratio of the generated video.",
    )
    duration: int = Field(
        default=6,
        ge=6,
        le=30,
        description="Duration of the generated video in seconds.",
    )
    resolution: Resolution = Field(
        default="480p",
        description="Resolution of the generated video.",
    )


class GrokImagineI2VPayload(BaseModel):
    model: str = "grok-imagine/image-to-video"
    input: InputSchema


class KieGrokImagineI2VAPI(KieAPI):
    def node_name(self) -> str:
        return "KieGrokImagineI2VNode"

    def set_payload(self, payload: dict):
        valid_payload = GrokImagineI2VPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
