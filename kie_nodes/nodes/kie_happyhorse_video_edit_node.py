from typing import Any, get_args

from ..api.happyhorse_video_edit_api import InputSchema, KieHappyHorseVideoEditAPI

_fields = InputSchema.model_fields


class KieHappyHorseVideoEditNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "video": ("VIDEO_URL",),
            },
            "optional": {
                "images": ("IMAGE_URL",),
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
                ),
                "audio_setting": (
                    list(get_args(_fields["audio_setting"].annotation)),
                    {"default": _fields["audio_setting"].default},
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

        api = KieHappyHorseVideoEditAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
