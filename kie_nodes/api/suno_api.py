from typing import Any, Literal

import requests
from pydantic import BaseModel, Field

from .base import KieAPI, get_api_key

SunoModel = Literal["V4", "V4_5", "V4_5PLUS", "V4_5ALL", "V5", "V5_5"]
VocalGender = Literal["m", "f"]
PersonaModelType = Literal["style_persona", "voice_persona"]


class SunoPayload(BaseModel):
    prompt: str = Field(
        ...,
        description="Description of desired audio content or lyrics in custom mode.",
        max_length=5000,
    )
    customMode: bool = Field(
        default=True,
        validation_alias="custom_mode",
        description="Enable advanced parameter customization.",
    )
    instrumental: bool = Field(
        default=True,
        description="Generate instrumental audio without vocals.",
    )
    model: SunoModel = Field(
        default="V5_5",
        description="AI model version to use for generation.",
    )
    style: str | None = Field(
        default=None,
        description="Music style (e.g. Jazz, Classical, Electronic).",
        max_length=1000,
    )
    title: str | None = Field(
        default=None,
        description="Title for the generated music track.",
        max_length=80,
    )
    negativeTags: str | None = Field(
        default=None,
        validation_alias="negative_tags",
        description="Music styles or traits to exclude from generation.",
    )
    vocalGender: VocalGender | None = Field(
        default=None,
        validation_alias="vocal_gender",
        description="Vocal gender preference: 'm' for male, 'f' for female.",
    )
    styleWeight: float | None = Field(
        default=None,
        validation_alias="style_weight",
        description="Strength of adherence to the specified style (0-1).",
        ge=0,
        le=1,
    )
    weirdnessConstraint: float | None = Field(
        default=None,
        validation_alias="weirdness_constraint",
        description="Controls experimental/creative deviation (0-1).",
        ge=0,
        le=1,
    )
    audioWeight: float | None = Field(
        default=None,
        validation_alias="audio_weight",
        description="Balance weight for audio features (0-1).",
        ge=0,
        le=1,
    )
    personaId: str | None = Field(
        default=None,
        validation_alias="persona_id",
        description="Persona ID or Voice ID to apply to the generated music.",
    )
    personaModel: PersonaModelType | None = Field(
        default=None,
        validation_alias="persona_model",
        description="Persona model type.",
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)


class KieSunoAPI(KieAPI):
    _task_endpoint: str = "https://api.kie.ai/api/v1/generate"
    _task_status_endpoint: str = "https://api.kie.ai/api/v1/generate/record-info"

    def node_name(self) -> str:
        return "KieSunoNode"

    def set_payload(self, payload: dict):
        # Filter empty strings for optional fields
        cleaned: dict = {}
        for k, v in payload.items():
            if isinstance(v, str) and v == "" and k != "prompt":
                continue
            cleaned[k] = v
        self._payload = SunoPayload(**cleaned)

    def get_task_status(self):
        if self._task_id is None:
            raise ValueError("Task ID is not set. Create a task first.")

        req = requests.get(
            f"{self._task_status_endpoint}?taskId={self._task_id}",
            headers={"Authorization": f"Bearer {get_api_key()}"},
        )
        req.raise_for_status()

        if req.status_code == 200:
            data: dict[str, Any] = req.json().get("data", {})
            status = data.get("status", "")

            if status == "SUCCESS":
                self._status = "success"
                self._result = data.get("response") or {}
            elif status in ("PENDING", "TEXT_SUCCESS", "FIRST_SUCCESS"):
                self._status = "pending"
            else:
                self._status = "failed"
                response = data.get("response") or {}
                self._fail_msg = (
                    response.get("errorMessage")
                    or data.get("errorMessage")
                    or f"Task failed with status: {status}"
                )

        return req.json()

    def get_audio_url(self) -> str:
        """Returns the first generated audio URL."""
        result = self.wait_for_task_completion()
        if not result:
            return ""
        suno_data = result.get("sunoData", [])
        if suno_data:
            return suno_data[0].get("audioUrl", "")
        return ""
