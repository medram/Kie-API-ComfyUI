from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import AudioUrls, ImageUrls, VideoUrls

Model = Literal[
    "bytedance/seedance-2",
    "bytedance/seedance-2-fast",
]

AspectRatio = Literal[
    "16:9",
    "4:3",
    "1:1",
    "3:4",
    "9:16",
    "21:9",
]

Resolution = Literal["480p", "720p", "1080p"]


class InputSchema(BaseModel):
    prompt: str = Field(
        default="",
        description="The text prompt or description for the video.",
        max_length=20000,
    )
    reference_image_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="A list of input image URLs.",
    )
    reference_video_urls: VideoUrls = Field(
        default_factory=list,
        validation_alias="videos",
        description=(
            "A list of input video URLs. The total length of the videos must "
            "not exceed 15 seconds."
        ),
    )
    reference_audio_urls: AudioUrls = Field(
        default_factory=list,
        validation_alias="audio",
        description=(
            "A list of input audio URLs. The total length of the audios must "
            "not exceed 15 seconds."
        ),
    )
    generate_audio: bool = Field(
        default=True,
        description="Whether to generate AI audio synchronized with the video.",
    )
    resolution: Resolution = Field(
        default="720p",
        description="The output video resolution.",
    )
    aspect_ratio: AspectRatio = Field(
        default="16:9",
        description="The aspect ratio of the generated video.",
    )
    duration: int = Field(
        default=15,
        ge=4,
        le=15,
        description="Video duration in seconds.",
    )
    web_search: bool = Field(
        default=False,
        description="Use online search.",
    )


class Seedance2Payload(BaseModel):
    model: Model = "bytedance/seedance-2"
    input: InputSchema


class KieSeedance2API(KieAPI):
    def node_name(self) -> str:
        return "KieSeedance2Node"

    def set_payload(self, payload: dict):
        model: Model = payload.pop("model", "bytedance/seedance-2")
        valid_payload = Seedance2Payload(model=model, input=InputSchema(**payload))
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
