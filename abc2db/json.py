import json

from pydantic import BaseModel

from .core import build_repository_impl, Repository


class Json(Repository):
    _model = BaseModel

    _self_add = ['_load', '_save']

    def __init__(self, path):
        self._path = path
        self._base = None
        self._id = 1

    def _load(self):
        with open(self._path, 'r') as file:
            base = json.loads(file.read())
        self._base = {
            int(k): self._model.parse_obj(v)
            for k, v in base.items()
        }
        if len(self._base.keys()) > 0:
            self._id = max(self._base.keys()) + 1

    def _save(self):
        with open(self._path, 'w') as file:
            file.write(json.dumps(
                {
                    str(k): v.dict()
                    for k, v in self._base.items()
                }
            ))

    def find(self, _id):
        self._load()
        return self._base.get(_id)

    def save(self, model):
        self._load()
        if model.id is None:
            model.id = self._id
            self._id += 1
        self._base[model.id] = model
        self._save()
        return model

    def save_all(self, models):
        return [
            self.save(i) for i in models
        ]

    def find_all(self, sort_key: [str] = None, desc: bool = False) -> list[BaseModel]:
        self._load()
        models = list(self._base.values())
        if sort_key:
            models.sort(key=lambda i: i.dict(include={sort_key})[sort_key], reverse=desc)
        return models

    def find_by(self, key: str, value, sort_key: [str] = None, desc: [bool] = None) -> list[BaseModel]:
        self._load()
        _models = list(self._base.values())
        models = []
        for i in _models:
            if i.dict(include={key})[key] == value:
                models.append(i)
        if sort_key:
            models.sort(key=lambda j: j.dict(include={sort_key})[sort_key], reverse=desc)
        return models

    def remove(self, model):
        self._load()
        self._base.pop(model.id)
        self._save()
        return model


def abc2db_json(abc_class: type) -> type:
    return build_repository_impl(abc_class, Json)
