from abc import ABC, abstractmethod

class IMessageQueue(ABC):
    @abstractmethod
    async def enqueue(self, video_id: str) -> str:
        """Encola job, retorna job_id"""
        pass

    @abstractmethod
    async def get_status(self, job_id: str) -> dict:
        """Estado de job"""
        pass

    @abstractmethod
    async def cancel(self, job_id: str) -> bool:
        """Cancela job"""
        pass

    @abstractmethod
    async def enqueue_batch(self, videos_data: list[dict]) -> str:
        """Encola un batch de importación"""
        pass

    @abstractmethod
    async def get_batch_status(self, job_id: str) -> dict:
        """Estado de un batch job"""
        pass
