from .nodes import (
    KieCrispUpscaleNode,
    KieGptImage2Node,
    KieGrokImagineI2VNode,
    KieGrokImagineT2INode,
    KieGrokImagineT2VNode,
    KieImageLoaderNode,
    KieImagePreviewNode,
    KieNanoBanana2Node,
    KieNanoBananaProNode,
    KieSeedance2Node,
    KieSeedream45Node,
    KieZImageNode,
    TextNode,
)

NODE_CLASS_MAPPINGS = {
    "KieGptImage2Node": KieGptImage2Node,
    "KieNanoBanana2Node": KieNanoBanana2Node,
    "KieNanoBananaProNode": KieNanoBananaProNode,
    "KieGrokImagineT2INode": KieGrokImagineT2INode,
    "KieGrokImagineI2VNode": KieGrokImagineI2VNode,
    "KieGrokImagineT2VNode": KieGrokImagineT2VNode,
    "KieCrispUpscaleNode": KieCrispUpscaleNode,
    "KieZImageNode": KieZImageNode,
    "KieSeedance2Node": KieSeedance2Node,
    "KieSeedream45Node": KieSeedream45Node,
    "KieImagePreviewNode": KieImagePreviewNode,
    "KieImageLoaderNode": KieImageLoaderNode,
    "TextNode": TextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextNode": "Text Node",
    "KieGptImage2Node": "Kie GPT Image 2",
    "KieNanoBanana2Node": "Kie NanoBanana 2",
    "KieNanoBananaProNode": "Kie NanoBanana Pro",
    "KieGrokImagineT2INode": "Kie Grok Imagine (T2I)",
    "KieGrokImagineI2VNode": "Kie Grok Imagine (I2V)",
    "KieGrokImagineT2VNode": "Kie Grok Imagine (T2V)",
    "KieCrispUpscaleNode": "Kie Crisp Upscale",
    "KieZImageNode": "Kie Z Image",
    "KieSeedance2Node": "Kie Seedance 2",
    "KieSeedream45Node": "Kie Seedream 4.5",
    "KieImagePreviewNode": "Kie Image Preview",
    "KieImageLoaderNode": "Kie Image Loader",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
