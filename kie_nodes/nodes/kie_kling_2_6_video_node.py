from typing import Any, get_args

from ..api.kling_2_6_video_api import (
    AspectRatio,
    Duration,
    InputSchema,
    KieKling26VideoAPI,
)
from .utils import save_preview_image

_fields = InputSchema.model_fields


class KieKling26VideoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "images": ("IMAGE_URL",),
                "sound": (
                    "BOOLEAN",
                    {"default": _fields["sound"].default},
                ),
                "aspect_ratio": (
                    list(get_args(AspectRatio)),
                    {"default": _fields["aspect_ratio"].default},
                ),
                "duration": (
                    list(get_args(Duration)),
                    {"default": _fields["duration"].default},
                ),
                "preview": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("VIDEO_URL",)
    RETURN_NAMES = ("Video",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Videos"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> dict[str, Any]:
        preview: bool = kwargs.pop("preview", True)
        payload = kwargs

        api = KieKling26VideoAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        result: dict = {"result": (video,)}

        if preview and video:
            preview_data = save_preview_image(video)
            result["ui"] = {"images": [preview_data]}

        return result
