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

    def find_by_id_sort_by_r_desc(self) -> list[User]:
        ...


UserRepositoryMemory = abc2db_memory(UserRepository)
repo: UserRepository = UserRepositoryMemory()

user1 = User(name='user1')
repo.save(user1)
print(user1)
print(repo.find(1))
