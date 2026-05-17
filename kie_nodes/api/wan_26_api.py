from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls, VideoUrls

Mode = Literal["T2V", "I2V", "V2V"]
Duration = Literal["5", "10", "15"]
Resolution = Literal["720p", "1080p"]

MODEL_MAP: dict[str, str] = {
    "T2V": "wan/2-6-text-to-video",
    "I2V": "wan/2-6-image-to-video",
    "V2V": "wan/2-6-video-to-video",
}


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="Text prompts for video generation.",
        max_length=5000,
    )
    image_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="Image URLs for I2V mode. All images must be at least 256x256px.",
    )
    video_urls: VideoUrls = Field(
        default_factory=list,
        validation_alias="videos",
        description="Video URLs for V2V mode.",
    )
    duration: Duration = Field(
        default="5",
        description="The duration of the generated video in seconds.",
    )
    resolution: Resolution = Field(
        default="1080p",
        description="Video resolution tier.",
    )
    multi_shots: bool = Field(
        default=False,
        description="Whether to use multiple shots with transitions.",
    )


class Wan26Payload(BaseModel):
    model: str = "wan/2-6-text-to-video"
    input: InputSchema


class KieWan26API(KieAPI):
    def node_name(self) -> str:
        return "KieWan26Node"

    def set_payload(self, payload: dict):
        mode: str = payload.pop("mode", "T2V")
        valid_payload = Wan26Payload(input=InputSchema(**payload))
        valid_payload.model = MODEL_MAP[mode]
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
