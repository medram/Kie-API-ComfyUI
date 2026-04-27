from .nodes import KieImageLoaderNode, KieImagePreviewNode, KieNanoBanana2Node

NODE_CLASS_MAPPINGS = {
    "KieNanoBanana2": KieNanoBanana2Node,
    "KieImagePreviewNode": KieImagePreviewNode,
    "KieImageLoaderNode": KieImageLoaderNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KieNanoBanana2": "KieNanoBanana2",
    "KieImagePreviewNode": "Kie Image Preview",
    "KieImageLoaderNode": "Kie Image Loader",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
