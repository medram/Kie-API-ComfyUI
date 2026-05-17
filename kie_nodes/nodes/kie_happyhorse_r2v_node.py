from typing import Any, get_args

from ..api.happyhorse_r2v_api import InputSchema, KieHappyHorseR2VAPI

_fields = InputSchema.model_fields


class KieHappyHorseR2VNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "images": ("IMAGE_URL",),
            },
            "optional": {
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
                        "min": 3,
                        "max": 15,
                        "step": 1,
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": _fields["seed"].default,
                        "min": 0,
                        "max": 2147483647,
                        "step": 1,
                    },
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

        api = KieHappyHorseR2VAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
