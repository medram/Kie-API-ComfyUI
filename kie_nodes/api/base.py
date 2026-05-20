import json
import os
import time
from abc import abstractmethod
from typing import Any, Literal

import requests
from comfy.model_management import (  # type: ignore
    throw_exception_if_processing_interrupted,
)
from comfy.utils import ProgressBar  # type: ignore
from pydantic import BaseModel, PrivateAttr

from ..log import _log


def _read_setting(key: str) -> str:
    """Read a value from ComfyUI's user settings file."""
    try:
        import folder_paths  # type: ignore

        user_dir = os.path.join(folder_paths.base_path, "user")
        settings_file = os.path.join(user_dir, "default", "comfy.settings.json")
        if os.path.isfile(settings_file):
            with open(settings_file, "r") as f:
                settings = json.load(f)
            return settings.get(key, "")
    except Exception:
        pass
    return ""


def get_api_key() -> str:
    # 1. Environment variable takes priority (Docker / headless / CI)
    api_key: str = os.environ.get("KIE_API_KEY", "")
    if api_key:
        return api_key

    # 2. Fall back to ComfyUI Settings panel value
    api_key = _read_setting("kie.api_key")
    if api_key:
        return api_key

    raise ValueError(
        "KIE API key is not configured. "
        "Set it in ComfyUI Settings (Kie API > API Key) "
        "or via the KIE_API_KEY environment variable."
    )


def get_openrouter_api_key() -> str:
    # 1. Environment variable takes priority (Docker / headless / CI)
    api_key: str = os.environ.get("OPENROUTER_API_KEY", "")
    if api_key:
        return api_key

    # 2. Fall back to ComfyUI Settings panel value
    api_key = _read_setting("kie.openrouter_api_key")
    if api_key:
        return api_key

    raise ValueError(
        "OpenRouter API key is not configured. "
        "Set it in ComfyUI Settings (Kie API > OpenRouter API Key) "
        "or via the OPENROUTER_API_KEY environment variable."
    )


class KieAPI(BaseModel):
    _payload: BaseModel | None = PrivateAttr(default=None)
    _task_id: str | None = PrivateAttr(default=None)
    _status: Literal["pending", "success", "failed"] | None = PrivateAttr(default=None)
    _result: dict[str, Any] | None = PrivateAttr(default=None)
    _fail_msg: str | None = PrivateAttr(default=None)
    _task_endpoint: str = "https://api.kie.ai/api/v1/jobs/create"
    _task_status_endpoint: str = "https://api.kie.ai/api/v1/jobs/recordInfo"

    def create_task(self):
        if self._payload is None:
            raise ValueError("Payload must be set before creating a task.")

        req = requests.post(
            self._task_endpoint,
            json=self._payload.model_dump(),
            headers={"Authorization": f"Bearer {get_api_key()}"},
        )

        req.raise_for_status()
        if req.status_code == 200:
            self._task_id = req.json().get("data", {}).get("taskId")
            if not self._task_id:
                raise ValueError(f"API did not return a taskId. Response: {req.text}")
        elif req.status_code in (401, 403):
            self._status = "failed"
            _log(f"[{self.node_name()}]: Unauthorized: Check your API key.")

        _log(f"[{self.node_name()}]: Created task with ID:", self._task_id)

    def get_task_status(self):
        if self._task_id is None:
            raise ValueError("Task ID is not set. Create a task first.")

        req = requests.get(
            f"{self._task_status_endpoint}?taskId={self._task_id}",
            headers={"Authorization": f"Bearer {get_api_key()}"},
        )
        req.raise_for_status()

        if req.status_code == 200:
            data: dict = req.json().get("data", {})
            if data.get("state") == "success" and data.get("resultJson"):
                self._status = "success"
                result: list | dict[str, Any] = json.loads(data["resultJson"])
                self._result = result if isinstance(result, dict) else None

            elif data.get("state") in ["waiting", "queuing", "generating"]:
                self._status = "pending"
            elif data.get("state") == "fail":
                self._status = "failed"
                self._fail_msg = data.get("failMsg") or "Task failed (unknown reason)"

        return req.json()

    def wait_for_task_completion(self) -> dict[str, Any] | None:
        if self._task_id is None:
            raise ValueError("Task ID is not set. Create a task first.")

        pbar = ProgressBar(100)
        pbar.update_absolute(5, 100)
        poll_count = 0

        time.sleep(5)  # Initial delay before polling

        while self._status == "pending" or self._status is None:
            throw_exception_if_processing_interrupted()
            self.get_task_status()
            _log(f"[{self.node_name()}]: Task {self._task_id}: generating...")
            poll_count += 1
            progress = min(5 + poll_count * 5, 95)
            pbar.update_absolute(progress, 100)
            time.sleep(5)  # Poll every 5 seconds

        _log(
            f"[{self.node_name()}]: Task {self._task_id} completed with status: {self._status}"
        )

        pbar.update_absolute(100, 100)

        if self._status == "failed":
            raise RuntimeError(f"[{self.node_name()}] Task failed: {self._fail_msg}")

        return self._result

    @abstractmethod
    def node_name(self) -> str:
        """Override this method in subclasses to return the name of the node for logging purposes."""
        return "KieAPIBaseNode"

    # def get_result(self) -> dict | list | None:
    #     if self._status == "success":
    #         return self._result

    #     raise ValueError(f"Task is not successful. Current status: {self._status}")
