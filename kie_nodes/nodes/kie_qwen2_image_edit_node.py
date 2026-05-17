from typing import Any, get_args

from ..api.qwen2_image_edit_api import InputSchema, KieQwen2ImageEditAPI
from .utils import save_preview_image

_fields = InputSchema.model_fields


class KieQwen2ImageEditNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {"multiline": True},
                ),
                "images": ("IMAGE_URL",),
            },
            "optional": {
                "image_size": (
                    list(get_args(_fields["image_size"].annotation)),
                    {"default": _fields["image_size"].default},
                ),
                "output_format": (
                    list(get_args(_fields["output_format"].annotation)),
                    {"default": _fields["output_format"].default},
                ),
                "seed": (
                    "INT",
                    {"default": _fields["seed"].default, "min": 0},
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

        api = KieQwen2ImageEditAPI()
        api.set_payload(payload)

        api.create_task()
        image: str = api.get_image_url()

        result: dict = {"result": (image,)}

        if preview and image:
            result["ui"] = {"images": [save_preview_image(image)]}

        return result
