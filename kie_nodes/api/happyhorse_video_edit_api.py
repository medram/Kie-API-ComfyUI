from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

Resolution = Literal["720p", "1080p"]

AudioSetting = Literal["auto", "origin"]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description=(
            "Edit instruction describing the intended change "
            "(e.g. style transfer / local replacement)."
        ),
        max_length=5000,
    )
    video_url: str = Field(
        default="",
        validation_alias="video",
        description=(
            "Input video URL. Duration: 3-60s. Resolution: long side <= 2160px, "
            "short side >= 320px. Aspect ratio: 1:2.5 to 2.5:1. Frame rate: > 8 fps."
        ),
    )
    reference_image: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="Optional reference image URL list (0-5).",
    )
    resolution: Resolution = Field(
        default="1080p",
        description="Output video resolution.",
    )
    audio_setting: AudioSetting = Field(
        default="auto",
        description="Audio handling strategy for the output video.",
    )
    seed: int = Field(
        default=0,
        ge=0,
        le=2147483647,
        description=("Random seed. If 0, the system generates a seed automatically."),
    )


class HappyHorseVideoEditPayload(BaseModel):
    model: str = "happyhorse/video-edit"
    input: InputSchema


class KieHappyHorseVideoEditAPI(KieAPI):
    def node_name(self) -> str:
        return "KieHappyHorseVideoEditNode"

    def set_payload(self, payload: dict):
        valid_payload = HappyHorseVideoEditPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
