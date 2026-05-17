from typing import Any, get_args

from ..api.grok_imagine_t2v_api import InputSchema, KieGrokImagineT2VAPI

_fields = InputSchema.model_fields


class KieGrokImagineT2VNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "mode": (
                    list(get_args(_fields["mode"].annotation)),
                    {"default": _fields["mode"].default},
                ),
                "aspect_ratio": (
                    list(get_args(_fields["aspect_ratio"].annotation)),
                    {"default": _fields["aspect_ratio"].default},
                ),
                "duration": (
                    "INT",
                    {
                        "default": _fields["duration"].default,
                        "min": 6,
                        "max": 30,
                        "step": 1,
                    },
                ),
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
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

        api = KieGrokImagineT2VAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
