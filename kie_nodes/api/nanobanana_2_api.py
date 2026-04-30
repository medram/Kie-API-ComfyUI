from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

AspectRatio = Literal[
    "1:1",
    "1:4",
    "1:8",
    "2:3",
    "3:2",
    "3:4",
    "4:1",
    "4:3",
    "4:5",
    "5:4",
    "8:1",
    "9:16",
    "16:9",
    "21:9",
    "auto",
]


class InputSchema(BaseModel):
    prompt: str = Field(
        ..., description="Text prompt to guide the image generation.", max_length=20000
    )
    aspect_ratio: AspectRatio = Field(
        default="auto",
        description="Aspect ratio of the output image, e.g., '1:1', '16:9', etc.",
    )
    resolution: Literal["1K", "2K", "4K"] = Field(
        default="1K",
        description="Resolution of the output image, e.g., '1K', '2K', '4K'.",
    )
    image_input: list[str] = Field(
        default_factory=list,
        max_items=14,
        description="Base64-encoded image input or URL to the image.",
    )
    output_format: Literal["png", "jpg"] = Field(
        default="png",
        description="Output image format, either 'png' or 'jpg'.",
    )


class NanoBanana2Payload(BaseModel):
    model: str = "nano-banana-2"
    input: InputSchema


class KieNanoBanana2API(KieAPI):
    def set_payload(self, payload: dict):

        # Validate and convert the input payload to the NanoBanana2Payload schema
        valid_payload = NanoBanana2Payload(
            input=payload
        )  # This will raise a validation error if the payload is invalid
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image URL."""
        # Wait for the task to complete and get the result
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
