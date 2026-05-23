from typing import Any, get_args

from ..api.grok_imagine_api import InputSchema, KieGrokImagineAPI
from .utils import save_preview_image

_fields = InputSchema.model_fields


class KieGrokImagineT2INode:
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
                "aspect_ratio": (
                    list(get_args(_fields["aspect_ratio"].annotation)),
                    {"default": _fields["aspect_ratio"].default},
                ),
                "enable_pro": (
                    "BOOLEAN",
                    {"default": _fields["enable_pro"].default},
                ),
                "preview": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE_URL",)
    RETURN_NAMES = ("Images",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Images"
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> tuple[list[str]] | dict[str, Any]:
        preview: bool = kwargs.pop("preview", True)
        payload = kwargs

        api = KieGrokImagineAPI()
        api.set_payload(payload)

        api.create_task()
        images: list[str] = api.get_image_urls()

        result: dict = {"result": (images,)}

        if preview and images:
            result["ui"] = {"images": [save_preview_image(url) for url in images]}

        return result
