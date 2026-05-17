import io
import os
import uuid
from typing import TypedDict

import folder_paths
import requests
from PIL import Image


class PreviewImage(TypedDict):
    filename: str
    subfolder: str
    type: str


def save_preview_image(image_url: str) -> PreviewImage:
    """Download an image URL and save it as a temp file for ComfyUI node preview."""
    response: requests.Response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    pil_image: Image.Image = Image.open(io.BytesIO(response.content)).convert("RGB")
    filename: str = f"kie_preview_{uuid.uuid4().hex}.png"
    temp_dir: str = folder_paths.get_temp_directory()
    os.makedirs(temp_dir, exist_ok=True)
    filepath: str = os.path.join(temp_dir, filename)
    pil_image.save(filepath, format="PNG")
    return PreviewImage(filename=filename, subfolder="", type="temp")
