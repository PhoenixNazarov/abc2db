from .async_core import AsyncRepository
from abc2db.core import build_repository_impl


class AsyncMemory(AsyncRepository):
    def __init__(self):
        self._base = {}
        self._id = 1

    async def find(self, _id):
        return self._base.get(_id)

    async def save(self, model):
        if model.id is None:
            model.id = self._id
            self._id += 1
        self._base[model.id] = model
        return model

    async def save_all(self, models):
        return [
            await self.save(i) for i in models
        ]

    async def find_all(self, sort_key: [str] = None, desc: bool = False):
        models = list(self._base.values())
        if sort_key:
            models.sort(key=lambda i: i.dict(include={sort_key})[sort_key], reverse=desc)
        return models

    async def find_by(self, key: str, value, sort_key: [str] = None, desc: [bool] = None):
        _models = list(self._base.values())
        models = []
        for i in _models:
            if i.dict(include={key})[key] == value:
                models.append(i)
        if sort_key:
            models.sort(key=lambda j: j.dict(include={sort_key})[sort_key], reverse=desc)
        return models

    async def remove(self, model):
        self._base.pop(model.id)
        return model


def abc2db_async_memory(abc_class: type) -> type:
    return build_repository_impl(abc_class, AsyncMemory)
