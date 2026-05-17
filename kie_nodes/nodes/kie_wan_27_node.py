from typing import Any, get_args

from ..api.wan_27_api import InputSchema, KieWan27API

_fields = InputSchema.model_fields


class KieWan27Node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "first_frame_image": ("IMAGE_URL",),
                "last_frame_image": ("IMAGE_URL",),
                "first_clip_video": ("VIDEO_URL",),
                "driving_audio": ("AUDIO_URL",),
                "audio": ("AUDIO_URL",),
                "resolution": (
                    list(get_args(_fields["resolution"].annotation)),
                    {"default": _fields["resolution"].default},
                ),
                "ratio": (
                    list(get_args(_fields["ratio"].annotation)),
                    {"default": _fields["ratio"].default},
                ),
                "duration": (
                    "INT",
                    {
                        "default": _fields["duration"].default,
                        "min": 2,
                        "max": 15,
                        "step": 1,
                    },
                ),
                "prompt_extend": (
                    "BOOLEAN",
                    {"default": _fields["prompt_extend"].default},
                ),
                "watermark": (
                    "BOOLEAN",
                    {"default": _fields["watermark"].default},
                ),
                "seed": (
                    "INT",
                    {"default": _fields["seed"].default, "min": 0, "max": 2147483647},
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

        api = KieWan27API()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
