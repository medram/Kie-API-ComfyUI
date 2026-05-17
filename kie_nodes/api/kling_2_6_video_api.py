from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls

Duration = Literal["5", "10"]
AspectRatio = Literal["1:1", "16:9", "9:16"]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="The text prompt used to generate the video.",
        max_length=2500,
    )
    image_urls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="Image URLs for I2V mode.",
    )
    sound: bool = Field(
        default=False,
        description="Whether the generated video contains sound.",
    )
    aspect_ratio: AspectRatio = Field(
        default="1:1",
        description="The aspect ratio of the video (T2V only).",
    )
    duration: Duration = Field(
        default="5",
        description="Duration of the video in seconds.",
    )


class Kling26VideoPayload(BaseModel):
    model: str = "kling-2.6/text-to-video"
    input: InputSchema


class KieKling26VideoAPI(KieAPI):
    def node_name(self) -> str:
        return "KieKling26VideoNode"

    def set_payload(self, payload: dict):
        valid_payload = Kling26VideoPayload(input=InputSchema(**payload))
        if valid_payload.input.image_urls:
            valid_payload.model = "kling-2.6/image-to-video"
        else:
            valid_payload.model = "kling-2.6/text-to-video"
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
