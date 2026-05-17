from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

Model = Literal["pro", "standard"]

MODEL_MAP: dict[str, str] = {
    "pro": "kling/ai-avatar-pro",
    "standard": "kling/ai-avatar-standard",
}


class InputSchema(BaseModel):
    prompt: str = Field(
        default="",
        description="The prompt to use for the video generation.",
        max_length=5000,
    )
    image_url: str = Field(
        ...,
        validation_alias="image",
        description="The URL of the image to use as your avatar.",
    )
    audio_url: str = Field(
        ...,
        validation_alias="audio",
        description="The URL of the audio file. The duration cannot exceed 5 minutes.",
    )


class KlingAiAvatarPayload(BaseModel):
    model: str = "kling/ai-avatar-pro"
    input: InputSchema


class KieKlingAiAvatarAPI(KieAPI):
    def node_name(self) -> str:
        return "KieKlingAiAvatarNode"

    def set_payload(self, payload: dict):
        model_key: str = payload.pop("model", "pro")
        valid_payload = KlingAiAvatarPayload(input=InputSchema(**payload))
        valid_payload.model = MODEL_MAP[model_key]
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
