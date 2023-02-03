from pydantic import BaseModel

from .core import build_repository_impl, Repository


class Memory(Repository):
    def __init__(self):
        self._base = {}
        self._id = 1

    def find(self, _id):
        return self._base.get(_id)

    def save(self, model):
        if model.id is None:
            model.id = self._id
            self._id += 1
        self._base[model.id] = model
        return model

    def save_all(self, models):
        return [
            self.save(i) for i in models
        ]

    def find_all(self, sort_key: [str] = None, desc: bool = False) -> list[BaseModel]:
        models = list(self._base.values())
        if sort_key:
            models.sort(key=lambda i: i.dict(include={sort_key})[sort_key], reverse=desc)
        return models

    def find_by(self, key: str, value, sort_key: [str] = None, desc: [bool] = None) -> list[BaseModel]:
        _models = list(self._base.values())
        models = []
        for i in _models:
            if i.dict(include={key})[key] == value:
                models.append(i)
        if sort_key:
            models.sort(key=lambda j: j.dict(include={sort_key})[sort_key], reverse=desc)
        return models


def abc2db_memory(abc_class: type) -> type:
    return build_repository_impl(abc_class, Memory)
