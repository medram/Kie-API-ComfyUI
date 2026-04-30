from typing import cast

from ..api.nanobanana_2_api import KieNanoBanana2API
from ..log import _log


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
                "resolution": (["1K", "2K", "4K"], {"default": "1K"}),
                "aspect_ratio": (
                    [
                        "1:1",
                        "1:4",
                        "1:8",
                        "2:3",
                        "3:2",
                        "3:4",
                        "4:1",
                        "4:3",
                        "4:5",
                        "5:4",
                        "8:1",
                        "9:16",
                        "16:9",
                        "21:9",
                        "auto",
                    ],
                    {"default": "auto"},
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
        result = cast(dict, nanobanana.wait_for_task_completion())

        print("Final result from NanoBanana2 API:", result)
        image: str = result.get("resultUrls", [""])[0] if result else ""

        _log("Received result from NanoBanana2 API:", image)

        # return (
        #     "https://fsn1.your-objectstorage.com/n8n-bucket/ytb/records/23/1773654208342-mpc70m8ovfp.png",
        # )
        return (image,)
