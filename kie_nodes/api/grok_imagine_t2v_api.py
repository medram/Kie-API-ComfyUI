from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

AspectRatio = Literal[
    "2:3",
    "3:2",
    "1:1",
    "9:16",
    "16:9",
]

Mode = Literal["fun", "normal", "spicy"]

Resolution = Literal["480p", "720p"]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="The text prompt describing the desired video motion.",
        max_length=5000,
    )
    aspect_ratio: AspectRatio = Field(
        default="2:3",
        description="Aspect ratio of the generated video.",
    )
    mode: Mode = Field(
        default="normal",
        description="Generation mode.",
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


class GrokImagineT2VPayload(BaseModel):
    model: str = "grok-imagine/text-to-video"
    input: InputSchema


class KieGrokImagineT2VAPI(KieAPI):
    def node_name(self) -> str:
        return "KieGrokImagineT2VNode"

    def set_payload(self, payload: dict):
        valid_payload = GrokImagineT2VPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
