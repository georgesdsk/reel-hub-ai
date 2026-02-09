from abc import ABC, abstractmethod
from typing import List

class IAIService(ABC):
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        pass

    @abstractmethod
    async def transcribe(self, audio_path: str) -> str:
        pass

    @abstractmethod
    async def categorize(self, transcript: str) -> dict:
        # Should return category, tags, ingredients, steps, etc.
        pass
