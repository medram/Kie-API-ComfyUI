from typing import Any, get_args

from ..api.seedance_1_5_pro_api import InputSchema, KieSeedance15ProAPI

_fields = InputSchema.model_fields


class KieSeedance15ProNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "images": ("IMAGE_URL",),
                "aspect_ratio": (
                    list(get_args(_fields["aspect_ratio"].annotation)),
                    {"default": _fields["aspect_ratio"].default},
                ),
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
                ),
                "duration": (
                    list(get_args(_fields["duration"].annotation)),
                    {"default": _fields["duration"].default},
                ),
                "fixed_lens": (
                    "BOOLEAN",
                    {"default": _fields["fixed_lens"].default},
                ),
                "generate_audio": (
                    "BOOLEAN",
                    {"default": _fields["generate_audio"].default},
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

        api = KieSeedance15ProAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
