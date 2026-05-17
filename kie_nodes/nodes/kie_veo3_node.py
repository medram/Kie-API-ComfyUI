from typing import Any, get_args

from ..api.veo3_api import KieVeo3API, Model, Veo3Payload

_fields = Veo3Payload.model_fields


class KieVeo3Node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "model": (list(get_args(Model)),),
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
                "enable_translation": (
                    "BOOLEAN",
                    {"default": _fields["enableTranslation"].default},
                ),
            },
        }

    RETURN_TYPES = ("VIDEO_URL",)
    RETURN_NAMES = ("Video",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Videos"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> dict[str, Any]:
        payload = kwargs

        api = KieVeo3API()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
