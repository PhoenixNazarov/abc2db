import os
import unittest
from abc import ABC, abstractmethod

from pydantic import BaseModel

from abc2db import abc2db_memory, abc2db_json


class User(BaseModel):
    id: int | None
    name: str
    ref_id: int | None = None


class UserRepository(ABC):
    @abstractmethod
    def find(self, _id) -> User:
        ...

    @abstractmethod
    def save(self, user: User) -> User:
        ...

    @abstractmethod
    def save_all(self, users: [User]) -> [User]:
        ...

    @abstractmethod
    def find_all(self) -> list[User]:
        ...

    @abstractmethod
    def find_all_sort_by_id(self) -> list[User]:
        ...

    @abstractmethod
    def find_all_sort_by_id_desc(self) -> list[User]:
        ...

    @abstractmethod
    def find_all_sort_by_ref_id(self) -> list[User]:
        ...

    @abstractmethod
    def find_all_sort_by_ref_id_desc(self) -> list[User]:
        ...

    @abstractmethod
    def find_by_ref_id(self, ref_id: int) -> list[User]:
        ...

    @abstractmethod
    def find_by_ref_id_sort_by_id(self, ref_id: int) -> list[User]:
        ...

    @abstractmethod
    def find_by_ref_id_sort_by_id_desc(self, ref_id: int) -> list[User]:
        ...


class TestRepositoryMemory(unittest.TestCase):
    def setUp(self) -> None:
        UserRepositoryMemory = abc2db_memory(UserRepository)
        with open('users.json', 'w') as file:
            file.write('{}')
        UserRepositoryJson = abc2db_json(UserRepository)

        self.repositories: list[UserRepository] = [
            UserRepositoryMemory(),
            UserRepositoryJson('users.json')
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('users.json')

    def test_build(self):
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                self.assertIsInstance(repo, UserRepository)

    def test_add(self):
        user1 = User(name='user1')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                repo.save(user1)
                self.assertEqual(repo.find(user1.id), user1)

    def test_save(self):
        user1 = User(name='user1')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                repo.save(user1)
                self.assertEqual(repo.find(user1.id), user1)
                user1.name = 'user2'
                self.assertEqual(repo.find(user1.id), user1)

    def test_save_all(self):
        user1 = User(name='user1')
        user2 = User(name='user2')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                repo.save_all([user1, user2])
                self.assertEqual(repo.find(user1.id), user1)
                self.assertEqual(repo.find(user2.id), user2)

    def test_add_id(self):
        user1 = User(name='user1')
        user2 = User(name='user2')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                repo.save_all([user1, user2])
                self.assertEqual(repo.find(user1.id), user1)
                self.assertEqual(repo.find(user2.id), user2)
                self.assertNotEqual(user1.id, user2.id)

    def test_get_all(self):
        user1 = User(name='user1')
        user2 = User(name='user2')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                repo.save_all([user1, user2])
                self.assertEqual(repo.find_all(), [user1, user2])
                self.assertEqual(repo.find_all_sort_by_id(), [user1, user2])
                self.assertEqual(repo.find_all_sort_by_id_desc(), [user2, user1])

    def test_get_all_sort(self):
        user1 = User(name='user1', ref_id=1)
        user2 = User(name='user2', ref_id=1)
        user3 = User(name='user3', ref_id=2)
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                repo.save_all([user1, user2, user3])
                self.assertEqual(repo.find_all_sort_by_ref_id(), [user1, user2, user3])
                self.assertEqual(repo.find_all_sort_by_ref_id_desc(), [user3, user1, user2])

    def test_find_by(self):
        user1 = User(name='user1', ref_id=1)
        user2 = User(name='user2', ref_id=1)
        user3 = User(name='user3', ref_id=2)
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                repo.save_all([user1, user2, user3])
                self.assertEqual(repo.find_by_ref_id(1), [user1, user2])
                self.assertEqual(repo.find_by_ref_id_sort_by_id(2), [user3])
                self.assertEqual(repo.find_by_ref_id_sort_by_id(1), [user1, user2])
                self.assertEqual(repo.find_by_ref_id_sort_by_id_desc(1), [user2, user1])
