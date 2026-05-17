from typing import Any, get_args

from ..api.kling_3_0_video_api import InputSchema, KieKling30VideoAPI, Mode

_fields = InputSchema.model_fields


class KieKling30VideoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (
                    list(get_args(Mode)),
                    {"default": _fields["mode"].default},
                ),
            },
            "optional": {},
        }

    RETURN_TYPES = ("VIDEO_URL",)
    RETURN_NAMES = ("Video",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Videos"
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> dict[str, Any]:
        payload = kwargs

        api = KieKling30VideoAPI()
        api.set_payload(payload)

        api.create_task()
        video: str = api.get_video_url()

        return {"result": (video,)}
