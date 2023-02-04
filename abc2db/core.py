from abc import ABC, abstractmethod
from typing import get_type_hints

from pydantic import BaseModel


class Repository(ABC):
    @abstractmethod
    def find(self, uid) -> [BaseModel]:
        """find model in base by uid"""

    @abstractmethod
    def save(self, model: BaseModel) -> BaseModel:
        """save model in base"""

    @abstractmethod
    def save_all(self, models: [BaseModel]) -> [BaseModel]:
        """save models in base"""

    @abstractmethod
    def find_all(self, sort_key: [str] = None, desc: [bool] = None) -> list[BaseModel]:
        """find all model in base"""

    @abstractmethod
    def find_by(self, key: str, value, sort_key: [str] = None, desc: [bool] = None) -> list[BaseModel]:
        """find in base by"""


def _find_sort_values(string: str) -> dict:
    vals = {
        'sort_key': None,
        'desc': False
    }
    if '_desc' in string:
        vals['desc'] = True
        string = string.replace('_desc', '')
    if 'sort_by' in string:
        vals['sort_key'] = string.split('sort_by_')[1]
    return vals


def wrap_get_all(repo_meth, sort_key, desc):
    def _wrap(self):
        return repo_meth(self, sort_key, desc)

    return _wrap


def wrap_find_by(repo_meth, by_key, sort_key, desc):
    def _wrap(self, v):
        return repo_meth(self, by_key, v, sort_key, desc)

    return _wrap


def build_repository_impl(abc_class, repository_impl) -> type:
    impl_dict = repository_impl.__dict__
    attrs = {
        '__init__': impl_dict['__init__'],
        '_model': get_type_hints(abc_class.__dict__['find'])['return']
    }

    for k, v in abc_class.__dict__.items():
        if k == 'find':
            attrs.update({'find': impl_dict['find']})
        elif k == 'save':
            attrs.update({'save': impl_dict['save']})
        elif k == 'save_all':
            attrs.update({'save_all': impl_dict['save_all']})
        elif k.startswith('find_by'):
            by_key = k.replace('find_by_', '').split('_sort_by')[0]
            sort_vals = _find_sort_values(k)
            attrs.update({
                k: wrap_find_by(impl_dict['find_by'], by_key, sort_vals['sort_key'], sort_vals['desc'])
            })
        elif k.startswith('find_all'):
            sort_vals = _find_sort_values(k)
            attrs.update({
                k: wrap_get_all(impl_dict['find_all'], sort_vals['sort_key'], sort_vals['desc'])
            })

    if '_self_add' in impl_dict:
        for j in impl_dict['_self_add']:
            attrs.update(
                {j: impl_dict[j]}
            )

    return type(
        abc_class.__name__ + repository_impl.__name__,
        (abc_class,),
        attrs
    )
