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
        ...,
        description=(
            "Text prompt describing the desired video. Use 'character1', "
            "'character2', etc. to refer to the corresponding images in order."
        ),
        max_length=5000,
    )
    reference_image: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description=(
            "Reference image URL list. Provide 1-9 images. The order defines "
            "which image is character1, character2, etc."
        ),
    )
    resolution: Resolution = Field(
        default="1080p",
        description="Output video resolution.",
    )
    aspect_ratio: AspectRatio = Field(
        default="16:9",
        description="Output aspect ratio.",
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


class HappyHorseR2VPayload(BaseModel):
    model: str = "happyhorse/reference-to-video"
    input: InputSchema


class KieHappyHorseR2VAPI(KieAPI):
    def node_name(self) -> str:
        return "KieHappyHorseR2VNode"

    def set_payload(self, payload: dict):
        valid_payload = HappyHorseR2VPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
