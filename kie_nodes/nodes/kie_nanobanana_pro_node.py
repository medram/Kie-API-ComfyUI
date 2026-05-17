from typing import Any, get_args

from ..api.nanobanana_pro_api import InputSchema, KieNanoBananaProAPI
from .utils import save_preview_image

_fields = InputSchema.model_fields


class KieNanoBananaProNode:
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
                "output_format": (
                    list(get_args(_fields["output_format"].annotation)),
                    {"default": _fields["output_format"].default},
                ),
                "preview": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE_URL",)
    RETURN_NAMES = ("Image",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Images"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> tuple[str] | dict[str, Any]:
        preview: bool = kwargs.pop("preview", True)
        payload = kwargs

        api = KieNanoBananaProAPI()
        api.set_payload(payload)

        api.create_task()
        image: str = api.get_image_url()

        result: dict = {"result": (image,)}

        if preview and image:
            result["ui"] = {"images": [save_preview_image(image)]}

        return result
