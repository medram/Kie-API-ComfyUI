from typing import Any

from ..api.recraft_crisp_upscale_api import KieCrispUpscaleAPI
from .utils import save_preview_image


class KieCrispUpscaleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE_URL",),
            },
            "optional": {
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

        api = KieCrispUpscaleAPI()
        api.set_payload(payload)

        api.create_task()
        image: str = api.get_image_url()

        result: dict = {"result": (image,)}

        if preview and image:
            result["ui"] = {"images": [save_preview_image(image)]}

        return result
