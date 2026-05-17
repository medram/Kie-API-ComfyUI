from typing import Any, get_args

from ..api.wan_22_animate_api import InputSchema, KieWan22AnimateAPI, Mode

_fields = InputSchema.model_fields


class KieWan22AnimateNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("VIDEO_URL",),
                "image": ("IMAGE_URL",),
                "mode": (list(get_args(Mode)),),
            },
            "optional": {
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
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

        api = KieWan22AnimateAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        result: dict = {"result": (video,)}

        if preview and video:
            from .utils import save_preview_image

            preview_data = save_preview_image(video)
            result["ui"] = {"images": [preview_data]}

        return result
