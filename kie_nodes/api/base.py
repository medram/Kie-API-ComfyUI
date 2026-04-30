import json
import os
import time
from abc import abstractmethod
from typing import Any, Literal

import requests
from comfy.utils import ProgressBar
from pydantic import BaseModel, PrivateAttr

from ..log import _log


def get_api_key() -> str:
    api_key: str = os.environ.get("KIE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "KIE_API_KEY environment variable is not set. "
            "Set it to your kie.ai API key before using this node."
        )
    return api_key


class KieAPI(BaseModel):
    _payload: BaseModel | None = PrivateAttr(default=None)
    _task_id: str | None = PrivateAttr(default=None)
    _status: Literal["pending", "success", "failed"] | None = PrivateAttr(default=None)
    _result: dict[str, Any] | None = PrivateAttr(default=None)

    def create_task(self):
        if self._payload is None:
            raise ValueError("Payload must be set before creating a task.")

        req = requests.post(
            "https://api.kie.ai/api/v1/jobs/createTask",
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
            f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={self._task_id}",
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

        return req.json()

    def wait_for_task_completion(self) -> dict[str, Any] | None:
        if self._task_id is None:
            raise ValueError("Task ID is not set. Create a task first.")

        pbar = ProgressBar(100)
        pbar.update_absolute(5, 100)
        poll_count = 0

        time.sleep(5)  # Initial delay before polling

        while self._status == "pending" or self._status is None:
            self.get_task_status()
            _log(f"[{self.node_name()}]: Task {self._task_id}: generating...")
            poll_count += 1
            progress = min(5 + poll_count * 5, 95)
            pbar.update_absolute(progress, 100)
            time.sleep(5)  # Poll every 5 seconds

        pbar.update_absolute(100, 100)
        return self._result

    @abstractmethod
    def node_name(self) -> str:
        """Override this method in subclasses to return the name of the node for logging purposes."""
        return "KieAPIBaseNode"

    # def get_result(self) -> dict | list | None:
    #     if self._status == "success":
    #         return self._result

    #     raise ValueError(f"Task is not successful. Current status: {self._status}")
