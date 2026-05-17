from typing import Any, get_args

from ..api.kling_ai_avatar_api import InputSchema, KieKlingAiAvatarAPI, Model

_fields = InputSchema.model_fields


class KieKlingAiAvatarNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE_URL",),
                "audio": ("AUDIO_URL",),
            },
            "optional": {
                "model": (
                    list(get_args(Model)),
                    {"default": "pro"},
                ),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("VIDEO_URL",)
    RETURN_NAMES = ("Video",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Videos"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> dict[str, Any]:
        payload = kwargs

        api = KieKlingAiAvatarAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
