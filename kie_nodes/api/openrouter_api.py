from __future__ import annotations

import requests

from ..log import _log
from .base import get_openrouter_api_key

_BASE_URL = "https://openrouter.ai/api/v1"
_MODELS_CACHE: list[dict] | None = None


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {get_openrouter_api_key()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/medram/Kie-API-ComfyUI",
        "X-OpenRouter-Title": "Kie API ComfyUI",
    }


def fetch_models() -> list[dict]:
    """Fetch available models from OpenRouter and cache the result."""
    global _MODELS_CACHE  # noqa: PLW0603
    if _MODELS_CACHE is not None:
        return _MODELS_CACHE
    try:
        resp = requests.get(
            f"{_BASE_URL}/models",
            timeout=15,
        )
        resp.raise_for_status()
        _MODELS_CACHE = resp.json().get("data", [])
    except Exception as exc:
        _log(f"[OpenRouter] Failed to fetch models: {exc}")
        _MODELS_CACHE = []
    return _MODELS_CACHE


def get_model_ids() -> list[str]:
    """Return a sorted list of model id slugs."""
    models = fetch_models()
    return sorted(m["id"] for m in models if m.get("id"))


def chat_completion(
    *,
    model: str,
    messages: list[dict],
    temperature: float | None = None,
    max_tokens: int | None = None,
    top_p: float | None = None,
    top_k: int | None = None,
    frequency_penalty: float | None = None,
    presence_penalty: float | None = None,
    repetition_penalty: float | None = None,
    min_p: float | None = None,
    top_a: float | None = None,
    seed: int | None = None,
    response_format: dict | None = None,
    stop: list[str] | None = None,
) -> dict:
    """Send a chat-completion request to OpenRouter and return the raw JSON response."""
    payload: dict = {
        "model": model,
        "messages": messages,
    }

    # Only include optional params when explicitly set
    if temperature is not None:
        payload["temperature"] = temperature
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if top_p is not None:
        payload["top_p"] = top_p
    if top_k is not None:
        payload["top_k"] = top_k
    if frequency_penalty is not None:
        payload["frequency_penalty"] = frequency_penalty
    if presence_penalty is not None:
        payload["presence_penalty"] = presence_penalty
    if repetition_penalty is not None:
        payload["repetition_penalty"] = repetition_penalty
    if min_p is not None:
        payload["min_p"] = min_p
    if top_a is not None:
        payload["top_a"] = top_a
    if seed is not None:
        payload["seed"] = seed
    if response_format is not None:
        payload["response_format"] = response_format
    if stop is not None:
        payload["stop"] = stop

    if not model or not model.strip():
        raise ValueError("[OpenRouter] Model must not be empty.")
    if not messages:
        raise ValueError("[OpenRouter] Messages must not be empty.")

    _log(f"[OpenRouter] Sending request to model: {model}")

    resp = requests.post(
        f"{_BASE_URL}/chat/completions",
        headers=_headers(),
        json=payload,
        timeout=300,
    )

    if resp.status_code == 401:
        raise RuntimeError(
            "[OpenRouter] Invalid API key. "
            "Check your key in ComfyUI Settings (Kie API > OpenRouter API Key) "
            "or the OPENROUTER_API_KEY environment variable."
        )
    if resp.status_code == 402:
        raise RuntimeError(
            "[OpenRouter] Insufficient credits. "
            "Please add credits at https://openrouter.ai/credits"
        )
    if resp.status_code == 429:
        raise RuntimeError(
            "[OpenRouter] Rate limit exceeded. Please wait and try again."
        )

    resp.raise_for_status()
    data: dict = resp.json()

    if "error" in data:
        err = data["error"]
        msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
        raise RuntimeError(f"[OpenRouter] API error: {msg}")

    return data
