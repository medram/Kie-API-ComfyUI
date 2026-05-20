from __future__ import annotations

import base64
import io
from typing import Any

import numpy as np
from PIL import Image

from ..api.openrouter_api import chat_completion, get_model_ids
from ..log import _log

# Fallback model list in case the API is unreachable at node-registration time
_FALLBACK_MODELS = [
    "anthropic/claude-sonnet-4",
    "anthropic/claude-opus-4",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-pro",
    "openai/gpt-4.1",
    "openai/gpt-4.1-mini",
    "openai/o3",
    "openai/o4-mini",
    "meta-llama/llama-4-maverick",
    "meta-llama/llama-4-scout",
    "deepseek/deepseek-r1",
    "deepseek/deepseek-chat-v3-0324",
    "mistralai/mistral-large",
    "qwen/qwen3-235b-a22b",
    "x-ai/grok-3",
]


def _get_models_for_dropdown() -> list[str]:
    """Get model list, falling back to a hardcoded list if the API call fails."""
    try:
        models = get_model_ids()
        if models:
            return models
    except Exception:
        pass
    return _FALLBACK_MODELS


def _tensor_to_base64(image_tensor: Any) -> str:
    """Convert a ComfyUI IMAGE tensor [B, H, W, C] to a base64-encoded PNG."""
    img = image_tensor[0]
    img_array = (img.cpu().numpy() * 255).astype(np.uint8)
    pil_image = Image.fromarray(img_array)
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


class KieOpenRouterNode:
    @classmethod
    def INPUT_TYPES(cls):
        models = _get_models_for_dropdown()
        return {
            "required": {
                "model": (models, {"default": models[0] if models else ""}),
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "system_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "placeholder": "Optional system instructions…",
                    },
                ),
                "image": ("IMAGE",),
                "image_url": ("IMAGE_URL",),
                "temperature": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05},
                ),
                "max_tokens": (
                    "INT",
                    {"default": 4096, "min": 1, "max": 200000, "step": 1},
                ),
                "top_p": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "top_k": (
                    "INT",
                    {"default": 0, "min": 0, "max": 500, "step": 1},
                ),
                "frequency_penalty": (
                    "FLOAT",
                    {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.05},
                ),
                "presence_penalty": (
                    "FLOAT",
                    {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.05},
                ),
                "repetition_penalty": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05},
                ),
                "min_p": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "top_a": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "seed": (
                    "INT",
                    {"default": 0, "min": 0, "max": 2**31 - 1, "step": 1},
                ),
                "json_mode": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Response",)
    FUNCTION = "generate"
    CATEGORY = "Kie API Nodes/LLM"
    OUTPUT_NODE = True

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs: Any) -> bool | str:
        model: str = kwargs.get("model", "")
        prompt: str = kwargs.get("prompt", "")
        image_url: str | None = kwargs.get("image_url")

        if not model or not model.strip():
            return "Model must be selected."

        if not prompt or not prompt.strip():
            return "Prompt cannot be empty."

        if image_url is not None and isinstance(image_url, str) and image_url.strip():
            url = image_url.strip()
            if not url.startswith(("http://", "https://")):
                return "Image URL must start with http:// or https://"

        return True

    def generate(self, **kwargs: Any) -> dict[str, Any]:
        model: str = kwargs["model"]
        prompt: str = kwargs["prompt"]
        system_prompt: str = kwargs.get("system_prompt", "")
        image = kwargs.get("image")
        image_url: str | None = kwargs.get("image_url")
        json_mode: bool = kwargs.get("json_mode", False)

        if not model.strip():
            raise ValueError("Model must be selected.")
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        # ----- build messages -----
        messages: list[dict] = []

        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})

        # Build user content (text + optional image for vision models)
        user_content: list[dict] | str
        has_image = image is not None or image_url

        if has_image:
            parts: list[dict] = []

            # Image from tensor
            if image is not None:
                b64 = _tensor_to_base64(image)
                parts.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}"},
                    }
                )

            # Image from URL
            if image_url:
                parts.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    }
                )

            parts.append({"type": "text", "text": prompt})
            user_content = parts
        else:
            user_content = prompt

        messages.append({"role": "user", "content": user_content})

        # ----- optional params (only send non-defaults) -----
        opt_params: dict[str, Any] = {}

        temperature = kwargs.get("temperature")
        if temperature is not None:
            opt_params["temperature"] = float(temperature)

        max_tokens = kwargs.get("max_tokens")
        if max_tokens is not None and int(max_tokens) > 0:
            opt_params["max_tokens"] = int(max_tokens)

        top_p = kwargs.get("top_p")
        if top_p is not None:
            opt_params["top_p"] = float(top_p)

        top_k = kwargs.get("top_k")
        if top_k is not None and int(top_k) > 0:
            opt_params["top_k"] = int(top_k)

        frequency_penalty = kwargs.get("frequency_penalty")
        if frequency_penalty is not None and float(frequency_penalty) != 0.0:
            opt_params["frequency_penalty"] = float(frequency_penalty)

        presence_penalty = kwargs.get("presence_penalty")
        if presence_penalty is not None and float(presence_penalty) != 0.0:
            opt_params["presence_penalty"] = float(presence_penalty)

        repetition_penalty = kwargs.get("repetition_penalty")
        if repetition_penalty is not None and float(repetition_penalty) != 1.0:
            opt_params["repetition_penalty"] = float(repetition_penalty)

        min_p = kwargs.get("min_p")
        if min_p is not None and float(min_p) > 0.0:
            opt_params["min_p"] = float(min_p)

        top_a = kwargs.get("top_a")
        if top_a is not None and float(top_a) > 0.0:
            opt_params["top_a"] = float(top_a)

        seed_val = kwargs.get("seed")
        if seed_val is not None and int(seed_val) > 0:
            opt_params["seed"] = int(seed_val)

        if json_mode:
            opt_params["response_format"] = {"type": "json_object"}

        # ----- call API -----
        data = chat_completion(model=model, messages=messages, **opt_params)

        # ----- extract response -----
        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError(
                f"[OpenRouter] No choices returned for model {model}. Response: {data}"
            )

        response_text: str = choices[0].get("message", {}).get("content", "")

        usage = data.get("usage", {})
        _log(
            f"[OpenRouter] Model: {model} | "
            f"Prompt tokens: {usage.get('prompt_tokens', '?')} | "
            f"Completion tokens: {usage.get('completion_tokens', '?')}"
        )

        return {"ui": {"text": [response_text]}, "result": (response_text,)}
