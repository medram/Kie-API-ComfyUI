import os
import uuid
from urllib.parse import urlparse

import folder_paths
import requests


class KieVideoPreviewNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("VIDEO_URL",),
            }
        }

    RETURN_TYPES = ("VIDEO_URL",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "preview"
    CATEGORY = "Kie API Nodes/Utility Nodes"
    OUTPUT_NODE = True

    def preview(self, video_url: str):
        if not video_url or not video_url.strip():
            raise ValueError("No video URL provided for preview.")

        parsed = urlparse(video_url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(f"Invalid video URL: '{video_url}'")

        response = requests.get(video_url, timeout=120, stream=True)
        response.raise_for_status()

        filename = f"kie_video_preview_{uuid.uuid4().hex}.mp4"
        temp_dir = folder_paths.get_temp_directory()
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return {
            "ui": {"videos": [{"filename": filename, "subfolder": "", "type": "temp"}]},
            "result": (video_url,),
        }
