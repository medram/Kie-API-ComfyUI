from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI

ElevenLabsTTSModel = Literal["multilingual-v2", "turbo-2.5"]

MODEL_MAP: dict[str, str] = {
    "multilingual-v2": "elevenlabs/text-to-speech-multilingual-v2",
    "turbo-2.5": "elevenlabs/text-to-speech-turbo-2-5",
}

Voice = Literal[
    "Rachel",
    "Aria",
    "Roger",
    "Sarah",
    "Laura",
    "Charlie",
    "George",
    "Callum",
    "River",
    "Liam",
    "Charlotte",
    "Alice",
    "Matilda",
    "Will",
    "Jessica",
    "Eric",
    "Chris",
    "Brian",
    "Daniel",
    "Lily",
    "Bill",
]


class InputSchema(BaseModel):
    text: str = Field(
        ...,
        description="The text to convert to speech.",
        max_length=5000,
    )
    voice: str = Field(
        default="Rachel",
        description="The voice to use for speech generation.",
    )
    stability: float = Field(
        default=0.5,
        description="Voice stability (0-1).",
        ge=0,
        le=1,
    )
    similarity_boost: float = Field(
        default=0.75,
        description="Similarity boost (0-1).",
        ge=0,
        le=1,
    )
    style: float = Field(
        default=0,
        description="Style exaggeration (0-1).",
        ge=0,
        le=1,
    )
    speed: float = Field(
        default=1,
        description="Speech speed (0.7-1.2).",
        ge=0.7,
        le=1.2,
    )
    language_code: str = Field(
        default="",
        description="Language code (ISO 639-1) to enforce a language.",
        max_length=500,
    )


class ElevenLabsTTSPayload(BaseModel):
    model: str = "elevenlabs/text-to-speech-multilingual-v2"
    input: InputSchema


class KieElevenLabsTTSAPI(KieAPI):
    def node_name(self) -> str:
        return "KieElevenLabsTTSNode"

    def set_payload(self, payload: dict):
        model_key: str = payload.pop("model", "multilingual-v2")
        valid_payload = ElevenLabsTTSPayload(input=InputSchema(**payload))
        valid_payload.model = MODEL_MAP.get(
            model_key, "elevenlabs/text-to-speech-multilingual-v2"
        )
        self._payload = valid_payload

    def get_audio_url(self) -> str:
        """Returns the generated audio URL."""
        result = self.wait_for_task_completion()
        if not result:
            return ""
        urls = result.get("resultUrls", [])
        return urls[0] if urls else ""
