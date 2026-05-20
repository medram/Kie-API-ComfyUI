import os

import folder_paths


class KieImageSelectUploadNode:
    """Node that lets you select/upload an image from your local PC and returns its public URL."""

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = sorted(
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        )
        return {
            "required": {
                "image": (files, {"image_upload": True}),
            },
        }

    DESCRIPTION = (
        "Select or upload an image from your local PC and get its public URL. "
        "Set the COMFYUI_PUBLIC_URL environment variable to your server's public address "
        "(e.g. https://your-domain.com). Defaults to http://127.0.0.1:8188."
    )
    RETURN_TYPES = ("IMAGE_URL",)
    RETURN_NAMES = ("image_url",)
    FUNCTION = "upload"
    CATEGORY = "Kie API Nodes/Utility Nodes"

    @classmethod
    def IS_CHANGED(cls, image):
        image_path = folder_paths.get_annotated_filepath(image)
        return os.path.getmtime(image_path)

    @classmethod
    def VALIDATE_INPUTS(cls, image):
        if not folder_paths.exists_annotated_filepath(image):
            return f"Invalid image file: {image}"
        return True

    def upload(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        # Determine subfolder and filename for the URL
        input_dir = folder_paths.get_input_directory()
        rel_path = os.path.relpath(image_path, input_dir)
        subfolder = os.path.dirname(rel_path)
        filename = os.path.basename(rel_path)

        base_url = os.environ.get("COMFYUI_PUBLIC_URL", "http://127.0.0.1:8188")
        base_url = base_url.rstrip("/")

        url = f"{base_url}/view?filename={filename}&type=input"
        if subfolder:
            url += f"&subfolder={subfolder}"

        return (url,)
