class TextNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {"multiline": True},
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Text",)
    FUNCTION = "process"
    CATEGORY = "Kie API Nodes/Utility Nodes"

    def process(self, text: str) -> tuple[str]:
        # Placeholder implementation - simply returns the input text
        return (text,)
