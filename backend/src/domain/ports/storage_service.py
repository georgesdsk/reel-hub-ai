from abc import ABC, abstractmethod

class IStorageService(ABC):
    @abstractmethod
    async def upload_file(self, file_path: str, destination: str) -> str:
        # Returns URL
        pass
