from typing import get_args

from ..api.nanobanana_2_api import InputSchema, KieNanoBanana2API

_fields = InputSchema.model_fields


class KieNanoBanana2Node:
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
                "image": ("IMAGE_URL",),
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
                ),
                "aspect_ratio": (
                    list(get_args(_fields["aspect_ratio"].annotation)),
                    {"default": _fields["aspect_ratio"].default},
                ),
            },
        }

    RETURN_TYPES = ("IMAGE_URL",)
    RETURN_NAMES = ("Image",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Images"
    # OUTPUT_IS_LIST = (True,)
    # INPUT_IS_LIST = True  # <--- THIS IS THE KEY

    def generate(self, *args, **kwargs) -> tuple[str]:
        # Placeholder implementation - replace with actual API call
        payload = kwargs

        nanobanana = KieNanoBanana2API()
        nanobanana.set_payload(payload)

        nanobanana.create_task()
        image: str = nanobanana.get_image_url()

        return (image,)
