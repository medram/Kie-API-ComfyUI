from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

AspectRatio = Literal[
    "16:9",
    "9:16",
    "1:1",
    "4:3",
    "3:4",
]

Resolution = Literal["720p", "1080p"]


class InputSchema(BaseModel):
    prompt: str = Field(
        default="",
        description="Text prompt describing the video to generate.",
        max_length=5000,
    )
    image_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description=(
            "First-frame image URL list. Exactly one image is required for I2V. "
            "Minimum resolution: width and height >= 300px. "
            "Aspect ratio: 1:2.5 to 2.5:1."
        ),
    )
    resolution: Resolution = Field(
        default="1080p",
        description="Output video resolution.",
    )
    aspect_ratio: AspectRatio = Field(
        default="16:9",
        description="Output aspect ratio (T2V only).",
    )
    duration: int = Field(
        default=5,
        ge=3,
        le=15,
        description="Output duration in seconds.",
    )
    seed: int = Field(
        default=0,
        ge=0,
        le=2147483647,
        description=("Random seed. If 0, the system generates a seed automatically."),
    )


class HappyHorsePayload(BaseModel):
    model: str = "happyhorse/text-to-video"
    input: InputSchema


class KieHappyHorseAPI(KieAPI):
    def node_name(self) -> str:
        return "KieHappyHorseNode"

    def set_payload(self, payload: dict):
        valid_payload = HappyHorsePayload(input=InputSchema(**payload))
        if valid_payload.input.image_urls:
            valid_payload.model = "happyhorse/image-to-video"
        else:
            valid_payload.model = "happyhorse/text-to-video"
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
