import unittest
from abc import ABC, abstractmethod

from pydantic import BaseModel

from abc2db import abc2db_memory


class User(BaseModel):
    id: int | None
    name: str


class UserRepository(ABC):
    @abstractmethod
    def find(self, _id) -> User:
        ...

    def save(self, user: User) -> User:
        ...


class TestRepositoryMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.UserRepositoryMemory = abc2db_memory(UserRepository)
        self.repo: UserRepository = self.UserRepositoryMemory()

    def test_build(self):
        self.assertIsInstance(self.repo, UserRepository)

    def test_add(self):
        user1 = User(name='user1')
        self.repo.save(user1)
        self.assertEqual(self.repo.find(user1.id), user1)
