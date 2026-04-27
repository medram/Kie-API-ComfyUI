import io
import os
import uuid

import folder_paths
import requests
from PIL import Image


class KieImagePreviewNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE_URL",),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "preview"
    CATEGORY = "Kie API Nodes/Images"
    OUTPUT_NODE = True
    INPUT_IS_LIST = True

    def preview(self, images: tuple[str]):
        if not images:
            raise ValueError("No image URLs provided for preview.")

        images_results = []

        for image in images:
            response = requests.get(image, timeout=30)
            response.raise_for_status()

            pil_image = Image.open(io.BytesIO(response.content)).convert("RGB")

            filename = f"kie_preview_{uuid.uuid4().hex}.png"
            temp_dir = folder_paths.get_temp_directory()
            os.makedirs(temp_dir, exist_ok=True)
            filepath = os.path.join(temp_dir, filename)
            pil_image.save(filepath, format="PNG")
            images_results.append(
                {"filename": filename, "subfolder": "", "type": "temp"}
            )

        return {"ui": {"images": images_results}}
