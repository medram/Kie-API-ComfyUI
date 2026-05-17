---
name: create-kie-node
description: "Create a new ComfyUI node from a Kie.ai API documentation URL. Use when: adding a new Kie API node, creating node from kie.ai docs, scaffolding API integration node, new model node."
argument-hint: "Paste the kie.ai model documentation URL (e.g. https://kie.ai/model/gpt-image-2-image-to-image.md)"
---

# Create Kie API Node from Documentation URL

## When to Use

- User provides a kie.ai model documentation URL and wants a new ComfyUI node
- Adding support for a new Kie.ai model to this project

## Naming Conventions

Use short suffixes for the task type:

| Task Type      | Suffix |
| -------------- | ------ |
| Image to Image | `I2I`  |
| Text to Image  | `T2I`  |
| Image to Video | `I2V`  |
| Text to Video  | `T2V`  |

Example: `KieGptImage2Node` (covers both T2I and I2I with automatic model inference)

## Multi-Variant Nodes (IMPORTANT)

When the same model has multiple variants that share the same payload structure (e.g. T2I and I2I differ only by model string and an optional `input_urls` field), **combine them into a single node** and **infer the model automatically** from the payload content.

Pattern:

- The API's `set_payload()` inspects the validated payload to choose the model string
- If reference images are present (`input_urls` is non-empty) → use the I2I model string
- If no reference images → use the T2I model string
- No `mode` selector is exposed to the user — inference is automatic
- The image input remains optional in the node

This keeps the node simple and the model selection transparent to the user.

## Procedure

### Step 1: Fetch the API documentation

Use `fetch_webpage` on the provided URL to extract:

- The `model` string (e.g. `"gpt-image-2-image-to-image"`)
- The `input` object parameters: name, type, required/optional, options (enum values), defaults
- The result structure from `resultJson` (e.g. `resultUrls` for images/video, `resultObject` for text)

All Kie.ai models share the same endpoints:

- **Create task**: `POST https://api.kie.ai/api/v1/jobs/createTask`
- **Query task**: `GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...`

These are already handled by the `KieAPI` base class — no need to change them.

### Step 2: Create the API file

Create `kie_nodes/api/<model_name>_api.py` following this template:

```python
from typing import Literal

from pydantic import BaseModel, Field

from .base import KieAPI
from .types import ImageUrls  # or VideoUrls, AudioUrls as needed


# Define Literal types for enum fields if needed (e.g. AspectRatio, Resolution)


class InputSchema(BaseModel):
    # Required fields first (no default)
    prompt: str = Field(..., description="...", max_length=20000)
    # Optional fields with defaults
    # For enum-like params, use Literal["opt1", "opt2"]
    # For image/file URL inputs, use the reusable types with validation_alias
    # to map the readable node input name to the API field name:
    # input_urls: ImageUrls = Field(
    #     default_factory=list,
    #     validation_alias="images",
    #     description="...",
    # )


class <ModelName>Payload(BaseModel):
    model: str = "<default-model-string>"
    input: InputSchema


class Kie<ModelName>API(KieAPI):
    def node_name(self) -> str:
        return "Kie<ModelName>Node"

    def set_payload(self, payload: dict):
        valid_payload = <ModelName>Payload(input=payload)
        # If the model has multiple variants (e.g. T2I/I2I), infer from payload:
        # if valid_payload.input.input_urls:
        #     valid_payload.model = "<model>-image-to-image"
        # else:
        #     valid_payload.model = "<model>-text-to-image"
        self._payload = valid_payload

    def get_image_url(self) -> str:
        """Returns the generated image/video URL."""
        result = self.wait_for_task_completion()
        return result.get("resultUrls", [""])[0] if result else ""
```

**Notes:**

- If the model only has ONE mode, skip `Mode`/`MODEL_MAP` and hardcode the model string
- For image/media/video output: use `result.get("resultUrls", [""])[0]` — return type `str`
- For multiple images: use `result.get("resultUrls", [])` — return type `list[str]`
- For text output: use `result.get("resultObject", {})` — return type `dict`
- Name the getter method appropriately: `get_image_url`, `get_video_url`, `get_result`, etc.

**Reusable types (`kie_nodes/api/types.py`):**

- `ImageUrls` — `Annotated[list[str], BeforeValidator(...)]` that coerces a single string to a list
- `VideoUrls` — same coercion for video URL fields
- `AudioUrls` — same coercion for audio URL fields
- Use these instead of raw `list[str]` for any URL list field that may receive a single string from ComfyUI

**`validation_alias` pattern:**

- Node inputs use readable names (e.g. `images`, `video`)
- API payloads use internal field names (e.g. `input_urls`, `image_input`)
- Use `validation_alias="<readable_name>"` on the Pydantic field so it accepts the node input name but serializes with the API field name
- Example: `input_urls: ImageUrls = Field(default_factory=list, validation_alias="images")`

### Step 3: Create the node file

Create `kie_nodes/nodes/kie_<model_name>_node.py` following this template:

```python
from typing import Any, get_args

from ..api.<api_module> import InputSchema, Kie<ModelName>API
from .utils import save_preview_image

_fields = InputSchema.model_fields


class Kie<ModelName>Node:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                # Image URL input (presence triggers I2I model inference):
                # Use plural "images" if API accepts multiple, singular "image" if only one
                "images": ("IMAGE_URL",),
                # Enum fields from InputSchema — use get_args to extract Literal options:
                # "resolution": (
                #     list(get_args(_fields["resolution"].annotation)),
                #     {"default": _fields["resolution"].default},
                # ),
                "preview": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE_URL",)  # or ("VIDEO_URL",), ("STRING",), etc.
    RETURN_NAMES = ("Image",)      # or ("Video",), ("Text",), etc.
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/Images"  # or /Videos, /Text, etc.
    OUTPUT_NODE = True

    def generate(self, *args, **kwargs) -> tuple[str] | dict[str, Any]:
        preview: bool = kwargs.pop("preview", True)
        payload = kwargs

        api = Kie<ModelName>API()
        api.set_payload(payload)

        api.create_task()
        image: str = api.get_image_url()

        result: dict = {"result": (image,)}

        if preview and image:
            preview = save_preview_image(image)
            result["ui"] = {"images": [preview]}

        return result
```

**INPUT_TYPES mapping rules:**

- `string` (required, text prompt) → `"STRING", {"multiline": True}` in `required`
- `string` with enum options → `list(get_args(_fields["field"].annotation)), {"default": _fields["field"].default}` in `optional`
- `array` of image/file URLs → `"IMAGE_URL"` in `optional` (maps to the custom IMAGE_URL type)
- All non-prompt fields should go in `optional`
- For nodes that generate images or videos, always include `"preview": ("BOOLEAN", {"default": True})` in `optional` to allow in-node preview

**In-node preview:**

- Nodes that generate images/videos must set `OUTPUT_NODE = True` and include the `preview` toggle
- Pop `preview` from kwargs before passing to the API: `preview: bool = kwargs.pop("preview", True)`
- Always return a dict with `"result"` key; conditionally add `"ui"` when `preview` is enabled
- Use `save_preview_image(url)` from `.utils` to download and save the image as a temp file for ComfyUI preview
- Import `save_preview_image` from `.utils` and `Any` from `typing`

**Singular vs plural naming:**

- If the API field accepts **multiple** items (e.g. `input_urls: list[str]`, `image_input: list[str]` with max_items > 1), use **plural** names: `"images"`, `"videos"`
- If the API field accepts only **one** item, use **singular**: `"image"`, `"video"`
- Same rule for outputs: if the result contains a single URL, use `"Image"` / `"Video"`; if multiple, use `"Images"` / `"Videos"`

### Step 4: Register the node

1. **`kie_nodes/nodes/__init__.py`**: Add the import and export
2. **`kie_nodes/__init__.py`**: Add to imports, `NODE_CLASS_MAPPINGS`, and `NODE_DISPLAY_NAME_MAPPINGS`

Display name format: `"Kie <Model Name> (<Type>)"` — e.g. `"Kie GPT Image 2 (I2I)"`

### Step 5: Verify

Check for errors in the created files to ensure no import or syntax issues.
