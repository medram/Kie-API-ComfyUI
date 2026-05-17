from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

Mode = Literal["Animate Move", "Animate Replace"]
Resolution = Literal["480p", "580p", "720p"]

MODEL_MAP: dict[str, str] = {
    "Animate Move": "wan/2-2-animate-move",
    "Animate Replace": "wan/2-2-animate-replace",
}


class InputSchema(BaseModel):
    video_url: str = Field(
        ...,
        validation_alias="video",
        description="URL of the input video.",
    )
    image_url: str = Field(
        ...,
        validation_alias="image",
        description=(
            "URL of the input image. If the input image does not match "
            "the chosen aspect ratio, it is resized and center cropped."
        ),
    )
    resolution: Resolution = Field(
        default="480p",
        description="Resolution of the generated video (480p, 580p, or 720p).",
    )


class Wan22AnimatePayload(BaseModel):
    model: str = "wan/2-2-animate-move"
    input: InputSchema


class KieWan22AnimateAPI(KieAPI):
    def node_name(self) -> str:
        return "KieWan22AnimateNode"

    def set_payload(self, payload: dict):
        mode: str = payload.pop("mode", "Animate Move")
        valid_payload = Wan22AnimatePayload(input=InputSchema(**payload))
        valid_payload.model = MODEL_MAP[mode]
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
