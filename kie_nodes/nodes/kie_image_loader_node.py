import io

import numpy as np
import requests
import torch
from PIL import Image


class KieImageLoaderNode:
    """Node to load images from URLs and convert them to tensors for processing in ComfyUI."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE_URL",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Images",)
    FUNCTION = "load"
    CATEGORY = "Kie API Nodes/Images"
    INPUT_IS_LIST = True

    def load(self, images: tuple[str]):
        if not images:
            raise ValueError("No image URLs provided for loading.")

        images_content = []

        for image in images:
            response = requests.get(image, timeout=30)
            response.raise_for_status()

            pil_image = Image.open(io.BytesIO(response.content)).convert("RGB")
            tensor = torch.from_numpy(np.array(pil_image).astype(np.float32) / 255.0)
            # ComfyUI expects shape [B, H, W, C]
            images_content.append(tensor.unsqueeze(0))

        return tuple(images_content)
