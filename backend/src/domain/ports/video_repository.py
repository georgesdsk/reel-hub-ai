from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.video import Video

class IVideoRepository(ABC):
    @abstractmethod
    async def save(self, video: Video) -> Video:
        pass

    @abstractmethod
    async def get_by_id(self, video_id: str) -> Optional[Video]:
        pass

    @abstractmethod
    async def search(self, query_embedding: List[float], limit: int = 10) -> List[Video]:
        pass

    @abstractmethod
    async def list_all(self, category: Optional[str] = None) -> List[Video]:
        pass
