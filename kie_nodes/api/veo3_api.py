from typing import Any, Literal

from pydantic import BaseModel, Field

from .base import KieAPI, get_api_key
from .types import ImageUrls

Model = Literal["veo3", "veo3_fast", "veo3_lite"]

AspectRatio = Literal["16:9", "9:16", "Auto"]

Resolution = Literal["720p", "1080p", "4k"]


class Veo3Payload(BaseModel):
    prompt: str = Field(
        ...,
        description="Text prompt describing the desired video content.",
        max_length=20000,
    )
    imageUrls: ImageUrls = Field(
        default_factory=list,
        validation_alias="images",
        description="Image URL list for image-to-video mode.",
    )
    model: Model = Field(
        default="veo3_fast",
        description="Model type to use.",
    )
    aspect_ratio: AspectRatio = Field(
        default="16:9",
        description="Video aspect ratio.",
    )
    resolution: Resolution = Field(
        default="720p",
        description="Output resolution.",
    )
    enableTranslation: bool = Field(
        default=True,
        validation_alias="enable_translation",
        description="Enable prompt translation to English.",
    )


class KieVeo3API(KieAPI):
    _task_endpoint: str = "https://api.kie.ai/api/v1/veo/generate"
    _task_status_endpoint: str = "https://api.kie.ai/api/v1/veo/record-info"

    def node_name(self) -> str:
        return "KieVeo3Node"

    def set_payload(self, payload: dict):
        valid_payload = Veo3Payload(**payload)
        self._payload = valid_payload

    def get_task_status(self):
        if self._task_id is None:
            raise ValueError("Task ID is not set. Create a task first.")

        import requests

        req = requests.get(
            f"{self._task_status_endpoint}?taskId={self._task_id}",
            headers={"Authorization": f"Bearer {get_api_key()}"},
        )
        req.raise_for_status()

        if req.status_code == 200:
            data: dict[str, Any] = req.json().get("data", {})
            flag = data.get("successFlag")

            if flag == 1:
                self._status = "success"
                self._result = data.get("response") or {}
            elif flag == 0:
                self._status = "pending"
            elif flag in (2, 3):
                self._status = "failed"
                self._fail_msg = (
                    data.get("errorMessage") or "Task failed (unknown reason)"
                )

        return req.json()

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
