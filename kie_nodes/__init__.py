from .nodes import (
    KieGptImage2Node,
    KieImageLoaderNode,
    KieImagePreviewNode,
    KieNanoBanana2Node,
    TextNode,
)

NODE_CLASS_MAPPINGS = {
    "KieGptImage2Node": KieGptImage2Node,
    "KieNanoBanana2Node": KieNanoBanana2Node,
    "KieImagePreviewNode": KieImagePreviewNode,
    "KieImageLoaderNode": KieImageLoaderNode,
    "TextNode": TextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextNode": "Text Node",
    "KieGptImage2Node": "Kie GPT Image 2",
    "KieNanoBanana2Node": "Kie NanoBanana 2",
    "KieImagePreviewNode": "Kie Image Preview",
    "KieImageLoaderNode": "Kie Image Loader",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
