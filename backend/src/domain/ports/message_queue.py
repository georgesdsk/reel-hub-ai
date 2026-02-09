from abc import ABC, abstractmethod

class IMessageQueue(ABC):
    @abstractmethod
    async def publish_task(self, task_name: str, payload: dict):
        pass
