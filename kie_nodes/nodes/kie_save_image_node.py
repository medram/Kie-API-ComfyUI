import io
import os
import uuid
from urllib.parse import urlparse

import folder_paths
import requests
from PIL import Image


class KieSaveImageNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE_URL",),
            },
            "optional": {
                "filename_prefix": (
                    "STRING",
                    {"default": "KieImage"},
                ),
            },
        }

    RETURN_TYPES = ("IMAGE_URL",)
    RETURN_NAMES = ("images",)
    FUNCTION = "save"
    CATEGORY = "Kie API Nodes/Utility Nodes"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)
    INPUT_IS_LIST = True

    def save(self, images: tuple[str], filename_prefix: list[str] | None = None):
        if not images:
            raise ValueError("No image URLs provided.")

        prefix = "KieImage"
        if filename_prefix and filename_prefix[0]:
            prefix = filename_prefix[0]

        images_results = []

        for image in images:
            if not image or not image.strip():
                continue
            parsed = urlparse(image)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(f"Invalid image URL: '{image}'")

            response = requests.get(image, timeout=30)
            response.raise_for_status()

            pil_image = Image.open(io.BytesIO(response.content)).convert("RGB")

            filename = f"{prefix}_{uuid.uuid4().hex}.png"
            output_dir = folder_paths.get_output_directory()
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            pil_image.save(filepath, format="PNG")
            images_results.append(
                {"filename": filename, "subfolder": "", "type": "output"}
            )

        return {"ui": {"images": images_results}, "result": (images,)}
