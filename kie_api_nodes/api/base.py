from pydantic import BaseModel, PrivateAttr


class KieAPI(BaseModel):
    _payload: BaseModel | None = PrivateAttr(default=None)

    def create_task(self): ...

    def get_task_result(self): ...
