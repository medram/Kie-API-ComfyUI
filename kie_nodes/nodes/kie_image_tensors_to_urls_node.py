import os
import uuid

import folder_paths
import numpy as np
from PIL import Image


class KieImageUploadNode:
    """Node that saves a ComfyUI IMAGE tensor and returns its public URL via the ComfyUI server."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    DESCRIPTION = (
        "Saves a ComfyUI image and returns its public URL. "
        "Set the COMFYUI_PUBLIC_URL environment variable to your server's public address "
        "(e.g. https://your-domain.com). Defaults to http://127.0.0.1:8188."
    )
    RETURN_TYPES = ("IMAGE_URL",)
    RETURN_NAMES = ("image_url",)
    FUNCTION = "upload"
    CATEGORY = "Kie API Nodes/Utility Nodes"

    def upload(self, image):
        # image is a tensor of shape [B, H, W, C] with values in [0, 1]
        # Take the first image in the batch
        img_tensor = image[0]
        img_array = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
        pil_image = Image.fromarray(img_array)

        filename = f"kie_upload_{uuid.uuid4().hex}.png"
        output_dir = folder_paths.get_output_directory()
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        pil_image.save(filepath, format="PNG")

        base_url = os.environ.get("COMFYUI_PUBLIC_URL", "http://127.0.0.1:8188")
        base_url = base_url.rstrip("/")
        image_url = f"{base_url}/view?filename={filename}&type=output"

        return (image_url,)
