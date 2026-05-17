from typing import Any, get_args

from ..api.suno_api import KieSunoAPI, SunoModel, SunoPayload, VocalGender

_fields = SunoPayload.model_fields


class KieSunoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "model": (
                    list(get_args(SunoModel)),
                    {"default": _fields["model"].default},
                ),
                "custom_mode": ("BOOLEAN", {"default": _fields["customMode"].default}),
                "instrumental": (
                    "BOOLEAN",
                    {"default": _fields["instrumental"].default},
                ),
                "style": ("STRING", {"default": ""}),
                "title": ("STRING", {"default": ""}),
                "negative_tags": ("STRING", {"default": ""}),
                "vocal_gender": (
                    ["none", *list(get_args(VocalGender))],
                    {"default": "none"},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Audio URL",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Audio"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> dict[str, Any]:
        # Remove sentinel values for optional enum fields
        if kwargs.get("vocal_gender") == "none":
            kwargs.pop("vocal_gender")

        payload = kwargs

        api = KieSunoAPI()
        api.set_payload(payload)

        api.create_task()
        audio_url: str = api.get_audio_url()

        return {"result": (audio_url,)}
