from ..api.nanobanana_2_api import KieNanoBanana2API


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
        image: str = nanobanana.get_image_url()
        print("NanoBanana2 API result:", image)

        return (image,)
