from abc import ABC, abstractmethod
from typing import Dict

class ModelTester(ABC):
    @abstractmethod
    def test(self, prompt: str) -> Dict:
        pass