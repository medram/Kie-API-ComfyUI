from typing import Any, get_args

from ..api.elevenlabs_tts_api import (
    ElevenLabsTTSModel,
    KieElevenLabsTTSAPI,
    Voice,
)


class KieElevenLabsTTSNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
            "optional": {
                "model": (
                    list(get_args(ElevenLabsTTSModel)),
                    {"default": "multilingual-v2"},
                ),
                "voice": (
                    list(get_args(Voice)),
                    {"default": "Rachel"},
                ),
                "stability": (
                    "FLOAT",
                    {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "similarity_boost": (
                    "FLOAT",
                    {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "style": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "speed": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.7, "max": 1.2, "step": 0.01},
                ),
                "language_code": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Audio URL",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Audio"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> dict[str, Any]:
        # Filter empty strings for optional fields
        if kwargs.get("language_code") == "":
            kwargs.pop("language_code")

        payload = kwargs

        api = KieElevenLabsTTSAPI()
        api.set_payload(payload)

        api.create_task()
        audio_url: str = api.get_audio_url()

        return {"result": (audio_url,)}
