import os
import unittest
from abc import ABC, abstractmethod

from pydantic import BaseModel

from abc2db.asyncio import abc2db_memory, abc2db_json


class User(BaseModel):
    id: int | None
    name: str
    ref_id: int | None = None


class UserRepository(ABC):
    @abstractmethod
    async def find(self, _id) -> User:
        ...

    @abstractmethod
    async def save(self, user: User) -> User:
        ...

    @abstractmethod
    async def save_all(self, users: [User]) -> [User]:
        ...

    @abstractmethod
    async def find_all(self) -> list[User]:
        ...

    @abstractmethod
    async def find_all_sort_by_id(self) -> list[User]:
        ...

    @abstractmethod
    async def find_all_sort_by_id_desc(self) -> list[User]:
        ...

    @abstractmethod
    async def find_all_sort_by_ref_id(self) -> list[User]:
        ...

    @abstractmethod
    async def find_all_sort_by_ref_id_desc(self) -> list[User]:
        ...

    @abstractmethod
    async def find_by_ref_id(self, ref_id: int) -> list[User]:
        ...

    @abstractmethod
    async def find_by_ref_id_sort_by_id(self, ref_id: int) -> list[User]:
        ...

    @abstractmethod
    async def find_by_ref_id_sort_by_id_desc(self, ref_id: int) -> list[User]:
        ...


class TestRepositoryMemory(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
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

    async def test_build(self):
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                self.assertIsInstance(repo, UserRepository)

    async def test_add(self):
        user1 = User(name='user1')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                await repo.save(user1)
                self.assertEqual(await repo.find(user1.id), user1)

    async def test_save(self):
        user1 = User(name='user1')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                await repo.save(user1)
                self.assertEqual(await repo.find(user1.id), user1)
                user1.name = 'user2'
                await repo.save(user1)
                self.assertEqual(await repo.find(user1.id), user1)

    async def test_save_all(self):
        user1 = User(name='user1')
        user2 = User(name='user2')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                await repo.save_all([user1, user2])
                self.assertEqual(await repo.find(user1.id), user1)
                self.assertEqual(await repo.find(user2.id), user2)

    async def test_add_id(self):
        user1 = User(name='user1')
        user2 = User(name='user2')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                await repo.save_all([user1, user2])
                self.assertEqual(await repo.find(user1.id), user1)
                self.assertEqual(await repo.find(user2.id), user2)
                self.assertNotEqual(user1.id, user2.id)

    async def test_get_all(self):
        user1 = User(name='user1')
        user2 = User(name='user2')
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                await repo.save_all([user1, user2])
                self.assertEqual(await repo.find_all(), [user1, user2])
                self.assertEqual(await repo.find_all_sort_by_id(), [user1, user2])
                self.assertEqual(await repo.find_all_sort_by_id_desc(), [user2, user1])

    async def test_get_all_sort(self):
        user1 = User(name='user1', ref_id=1)
        user2 = User(name='user2', ref_id=1)
        user3 = User(name='user3', ref_id=2)
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                await repo.save_all([user1, user2, user3])
                self.assertEqual(await repo.find_all_sort_by_ref_id(), [user1, user2, user3])
                self.assertEqual(await repo.find_all_sort_by_ref_id_desc(), [user3, user1, user2])

    async def test_find_by(self):
        user1 = User(name='user1', ref_id=1)
        user2 = User(name='user2', ref_id=1)
        user3 = User(name='user3', ref_id=2)
        for repo in self.repositories:
            with self.subTest(msg=f'{type(repo)}'):
                await repo.save_all([user1, user2, user3])
                self.assertEqual(await repo.find_by_ref_id(1), [user1, user2])
                self.assertEqual(await repo.find_by_ref_id_sort_by_id(2), [user3])
                self.assertEqual(await repo.find_by_ref_id_sort_by_id(1), [user1, user2])
                self.assertEqual(await repo.find_by_ref_id_sort_by_id_desc(1), [user2, user1])
