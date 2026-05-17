from typing import Any, get_args

from ..api.gpt_image_2_api import InputSchema, KieGptImage2API
from .utils import save_preview_image

_fields = InputSchema.model_fields


class KieGptImage2Node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {"multiline": True},
                ),
            },
            "optional": {
                "images": ("IMAGE_URL",),
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
                ),
                "aspect_ratio": (
                    list(get_args(_fields["aspect_ratio"].annotation)),
                    {"default": _fields["aspect_ratio"].default},
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

        api = KieGptImage2API()
        api.set_payload(payload)

        api.create_task()
        image: str = api.get_image_url()

        result: dict = {"result": (image,)}

        if preview and image:
            result["ui"] = {"images": [save_preview_image(image)]}

        return result
