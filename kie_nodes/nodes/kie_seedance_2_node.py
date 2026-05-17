from typing import Any, get_args

from ..api.seedance_2_api import InputSchema, KieSeedance2API, Model

_fields = InputSchema.model_fields


class KieSeedance2Node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (list(get_args(Model)),),
            },
            "optional": {
                "prompt": (
                    "STRING",
                    {"multiline": True, "default": _fields["prompt"].default},
                ),
                "images": ("IMAGE_URL",),
                "videos": ("VIDEO_URL",),
                "audio": ("AUDIO_URL",),
                "generate_audio": (
                    "BOOLEAN",
                    {"default": _fields["generate_audio"].default},
                ),
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
                ),
                "aspect_ratio": (
                    list(get_args(_fields["aspect_ratio"].annotation)),
                    {"default": _fields["aspect_ratio"].default},
                ),
                "duration": (
                    "INT",
                    {
                        "default": _fields["duration"].default,
                        "min": 4,
                        "max": 15,
                        "step": 1,
                    },
                ),
                "web_search": (
                    "BOOLEAN",
                    {"default": _fields["web_search"].default},
                ),
            },
        }

    RETURN_TYPES = ("VIDEO_URL",)
    RETURN_NAMES = ("Video",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Videos"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> dict[str, Any]:
        payload = kwargs

        api = KieSeedance2API()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
