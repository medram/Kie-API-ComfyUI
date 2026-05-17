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


class InputSchema(BaseModel):
    prompt: str = Field(
        ..., description="Text prompt to guide the image generation.", max_length=5000
    )
    aspect_ratio: AspectRatio = Field(
        default="3:2",
        description="Specifies the width-to-height ratio of the generated image.",
    )
    enable_pro: bool = Field(
        default=False,
        description=(
            "Toggle for request processing mode. false enables speed mode "
            "(prioritizes low latency); true enables quality mode "
            "(prioritizes output quality)."
        ),
    )


class GrokImaginePayload(BaseModel):
    model: str = "grok-imagine/text-to-image"
    input: InputSchema


class KieGrokImagineAPI(KieAPI):
    def node_name(self) -> str:
        return "KieGrokImagineT2INode"

    def set_payload(self, payload: dict):
        valid_payload = GrokImaginePayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
