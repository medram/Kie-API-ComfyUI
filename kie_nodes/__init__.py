import os
import shutil

import folder_paths
from aiohttp import web
from server import PromptServer

from .nodes import (
    KieCrispUpscaleNode,
    KieElevenLabsTTSNode,
    KieGptImage2Node,
    KieGrokImagineI2VNode,
    KieGrokImagineT2INode,
    KieGrokImagineT2VNode,
    KieHappyHorseNode,
    KieHappyHorseR2VNode,
    KieHappyHorseVideoEditNode,
    KieImageLoaderNode,
    KieImagePickerNode,
    KieImagePreviewNode,
    KieImageSelectUploadNode,
    KieImageUploadNode,
    KieKling26VideoNode,
    KieKling30VideoNode,
    KieKlingAiAvatarNode,
    KieNanoBanana2Node,
    KieNanoBananaProNode,
    KieOpenRouterNode,
    KieQwen2ImageEditNode,
    KieSaveImageNode,
    KieSeedance2Node,
    KieSeedance15ProNode,
    KieSeedream5LiteNode,
    KieSeedream45Node,
    KieSunoNode,
    KieVeo3Node,
    KieVideoPreviewNode,
    KieWan22AnimateNode,
    KieWan26Node,
    KieWan27Node,
    KieZImageNode,
    TextNode,
)

NODE_CLASS_MAPPINGS = {
    "KieGptImage2Node": KieGptImage2Node,
    "KieNanoBanana2Node": KieNanoBanana2Node,
    "KieNanoBananaProNode": KieNanoBananaProNode,
    "KieOpenRouterNode": KieOpenRouterNode,
    "KieGrokImagineT2INode": KieGrokImagineT2INode,
    "KieGrokImagineI2VNode": KieGrokImagineI2VNode,
    "KieGrokImagineT2VNode": KieGrokImagineT2VNode,
    "KieHappyHorseNode": KieHappyHorseNode,
    "KieHappyHorseR2VNode": KieHappyHorseR2VNode,
    "KieHappyHorseVideoEditNode": KieHappyHorseVideoEditNode,
    "KieCrispUpscaleNode": KieCrispUpscaleNode,
    "KieElevenLabsTTSNode": KieElevenLabsTTSNode,
    "KieZImageNode": KieZImageNode,
    "KieKling26VideoNode": KieKling26VideoNode,
    "KieKling30VideoNode": KieKling30VideoNode,
    "KieKlingAiAvatarNode": KieKlingAiAvatarNode,
    "KieSeedance15ProNode": KieSeedance15ProNode,
    "KieSeedance2Node": KieSeedance2Node,
    "KieQwen2ImageEditNode": KieQwen2ImageEditNode,
    "KieSeedream45Node": KieSeedream45Node,
    "KieSeedream5LiteNode": KieSeedream5LiteNode,
    "KieVeo3Node": KieVeo3Node,
    "KieVideoPreviewNode": KieVideoPreviewNode,
    "KieWan22AnimateNode": KieWan22AnimateNode,
    "KieWan26Node": KieWan26Node,
    "KieWan27Node": KieWan27Node,
    "KieSunoNode": KieSunoNode,
    "KieImagePreviewNode": KieImagePreviewNode,
    "KieImageLoaderNode": KieImageLoaderNode,
    "KieImagePickerNode": KieImagePickerNode,
    "KieImageSelectUploadNode": KieImageSelectUploadNode,
    "KieImageUploadNode": KieImageUploadNode,
    "KieSaveImageNode": KieSaveImageNode,
    "TextNode": TextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextNode": "📝 Text Node",
    "KieGptImage2Node": "🎨 Kie GPT Image 2",
    "KieNanoBanana2Node": "🍌 Kie NanoBanana 2",
    "KieNanoBananaProNode": "🍌 Kie NanoBanana Pro",
    "KieOpenRouterNode": "🧠 Kie OpenRouter LLM",
    "KieGrokImagineT2INode": "🖼️ Kie Grok Imagine (T2I)",
    "KieGrokImagineI2VNode": "🎬 Kie Grok Imagine (I2V)",
    "KieGrokImagineT2VNode": "🎬 Kie Grok Imagine (T2V)",
    "KieHappyHorseNode": "🐴 Kie HappyHorse Video",
    "KieHappyHorseR2VNode": "🐴 Kie HappyHorse (R2V)",
    "KieHappyHorseVideoEditNode": "🐴 Kie HappyHorse Video Edit",
    "KieCrispUpscaleNode": "🔍 Kie Crisp Upscale",
    "KieElevenLabsTTSNode": "🔊 Kie ElevenLabs TTS",
    "KieZImageNode": "🖼️ Kie Z Image",
    "KieKling26VideoNode": "🎥 Kie Kling 2.6 Video",
    "KieKling30VideoNode": "🎥 Kie Kling 3.0 Video",
    "KieKlingAiAvatarNode": "👤 Kie Kling AI Avatar",
    "KieSeedance15ProNode": "💃 Kie Seedance 1.5 Pro",
    "KieSeedance2Node": "💃 Kie Seedance 2",
    "KieQwen2ImageEditNode": "✏️ Kie Qwen2 Image Edit",
    "KieSeedream45Node": "🌄 Kie Seedream 4.5",
    "KieSeedream5LiteNode": "🌄 Kie Seedream 5 Lite",
    "KieVeo3Node": "📹 Kie Veo 3",
    "KieVideoPreviewNode": "▶️ Kie Video Preview",
    "KieWan22AnimateNode": "✨ Kie Wan 2.2 Animate",
    "KieWan26Node": "🎞️ Kie Wan 2.6",
    "KieWan27Node": "🎞️ Kie Wan 2.7",
    "KieSunoNode": "🎵 Kie Suno Music",
    "KieImagePreviewNode": "👁️ Kie Image Preview",
    "KieImageLoaderNode": "⬇️ Kie Image (URLs to Tensors)",
    "KieImagePickerNode": "🖼️ Kie Image Picker",
    "KieImageSelectUploadNode": "📂 Kie Image Loader",
    "KieImageUploadNode": "⬆️ Kie Image (Tensors to URLs)",
    "KieSaveImageNode": "💾 Kie Save Image",
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]


# --- Server route for saving preview images to output ---


@PromptServer.instance.routes.post("/kie/save_image")
async def kie_save_image_route(request: web.Request) -> web.Response:
    data = await request.json()
    images = data.get("images", [])

    saved = 0
    for img in images:
        filename = img.get("filename", "")

        # Security: reject path traversal attempts
        if not filename or ".." in filename or "/" in filename or "\\" in filename:
            continue

        temp_dir = folder_paths.get_temp_directory()
        output_dir = folder_paths.get_output_directory()

        src = os.path.join(temp_dir, filename)

        # Verify resolved path stays inside temp directory
        if not os.path.realpath(src).startswith(os.path.realpath(temp_dir)):
            continue

        if not os.path.isfile(src):
            continue

        os.makedirs(output_dir, exist_ok=True)
        dst = os.path.join(output_dir, filename)
        shutil.copy2(src, dst)
        saved += 1

    return web.json_response({"success": True, "saved": saved})
