from abc import ABC, abstractmethod
from typing import Optional


class Bookmarker(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass
