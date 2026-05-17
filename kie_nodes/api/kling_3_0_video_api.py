from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

Mode = Literal["std", "pro", "4K"]


class InputSchema(BaseModel):
    mode: Mode = Field(
        default="std",
        description=(
            "Generation mode. std has standard resolution, pro has higher resolution."
        ),
    )


class Kling30VideoPayload(BaseModel):
    model: str = "kling-3.0/video"
    input: InputSchema


class KieKling30VideoAPI(KieAPI):
    def node_name(self) -> str:
        return "KieKling30VideoNode"

    def set_payload(self, payload: dict):
        valid_payload = Kling30VideoPayload(input=InputSchema(**payload))
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
