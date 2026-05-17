from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

Resolution = Literal["720p", "1080p"]
Ratio = Literal["16:9", "9:16", "1:1", "4:3", "3:4"]


class InputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description="The positive prompt for the generation.",
        max_length=5000,
    )
    negative_prompt: str = Field(
        default="",
        description="The negative prompt for the generation.",
        max_length=500,
    )
    first_frame_url: str = Field(
        default="",
        validation_alias="first_frame_image",
        description="First frame image URL (triggers I2V mode).",
    )
    last_frame_url: str = Field(
        default="",
        validation_alias="last_frame_image",
        description="Last frame image URL.",
    )
    first_clip_url: str = Field(
        default="",
        validation_alias="first_clip_video",
        description="Video clip URL to guide generation.",
    )
    driving_audio_url: str = Field(
        default="",
        validation_alias="driving_audio",
        description="Audio URL for I2V generation.",
    )
    audio_url: str = Field(
        default="",
        validation_alias="audio",
        description="Audio URL for T2V generation.",
    )
    resolution: Resolution = Field(
        default="1080p",
        description="The resolution of output.",
    )
    ratio: Ratio = Field(
        default="16:9",
        description="The ratio of output (T2V only).",
    )
    duration: int = Field(
        default=5,
        ge=2,
        le=15,
        description="Total duration of output in seconds.",
    )
    prompt_extend: bool = Field(
        default=True,
        description="Whether to enable the prompt optimizer.",
    )
    watermark: bool = Field(
        default=False,
        description="Whether to enable the watermark.",
    )
    seed: int = Field(
        default=0,
        ge=0,
        le=2147483647,
        description="The random seed for reproducible generation.",
    )


class Wan27Payload(BaseModel):
    model: str = "wan/2-7-text-to-video"
    input: InputSchema


class KieWan27API(KieAPI):
    def node_name(self) -> str:
        return "KieWan27Node"

    def set_payload(self, payload: dict):
        valid_payload = Wan27Payload(input=InputSchema(**payload))
        # Infer model: if any image/video frame input is provided → I2V
        inp = valid_payload.input
        if inp.first_frame_url or inp.last_frame_url or inp.first_clip_url:
            valid_payload.model = "wan/2-7-image-to-video"
        else:
            valid_payload.model = "wan/2-7-text-to-video"
        self._payload = valid_payload

    def get_video_url(self) -> str:
        """Returns the generated video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
