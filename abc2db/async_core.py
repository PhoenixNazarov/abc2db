from abc import ABC, abstractmethod
from typing import Callable

from pydantic import BaseModel


class AsyncRepository(ABC):
    @abstractmethod
    async def find(self, uid) -> [BaseModel]:
        """find model in base by uid"""

    @abstractmethod
    async def save(self, model: BaseModel) -> BaseModel:
        """save model in base"""

    @abstractmethod
    async def save_all(self, models: [BaseModel]) -> [BaseModel]:
        """save models in base"""

    @abstractmethod
    async def find_all(self, sort_key: [Callable] = None, desc: [bool] = None) -> list[BaseModel]:
        """find all model in base"""

    @abstractmethod
    async def find_by(self, key: str, value, sort_key: [Callable] = None, desc: [bool] = None) -> list[BaseModel]:
        """find in base by"""

    @abstractmethod
    async def remove(self, model: BaseModel):
        """remove model from base"""
