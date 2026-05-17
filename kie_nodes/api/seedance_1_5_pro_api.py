from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

AspectRatio = Literal[
    "1:1",
    "21:9",
    "4:3",
    "3:4",
    "16:9",
    "9:16",
]

Resolution = Literal["480p", "720p", "1080p"]

Duration = Literal["4", "8", "12"]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="Enter video description (3-2500 characters).",
        max_length=2500,
    )
    input_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="Upload 0-2 images. Leave empty to generate video from text only.",
    )
    aspect_ratio: AspectRatio = Field(
        default="16:9",
        description="Select the frame dimensions.",
    )
    resolution: Resolution = Field(
        default="720p",
        description="Standard (480p) / High (720p) / 1080p.",
    )
    duration: Duration = Field(
        default="8",
        description="Video duration: 4s / 8s / 12s.",
    )
    fixed_lens: bool = Field(
        default=False,
        description=(
            "Enable to keep the camera view static and stable. "
            "Disable for dynamic camera movement."
        ),
    )
    generate_audio: bool = Field(
        default=False,
        description=(
            "Enable to create sound effects for the video (additional cost applies)."
        ),
    )


class Seedance15ProPayload(BaseModel):
    model: str = "bytedance/seedance-1.5-pro"
    input: InputSchema


class KieSeedance15ProAPI(KieAPI):
    def node_name(self) -> str:
        return "KieSeedance15ProNode"

    def set_payload(self, payload: dict):
        valid_payload = Seedance15ProPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
