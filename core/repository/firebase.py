from typing import Any

from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable

import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1 import document
from loguru import logger


class BaseFirebaseRepository:
    _firebase_app = None

    def __init__(self, credentials: dict[Any, Any]) -> None:
        cred = firebase_admin.credentials.Certificate(credentials)

        if self._firebase_app is None:
            self._firebase_app = firebase_admin.initialize_app(cred)

        self.client = firestore.Client()


class UserRepository(ABC):
    @abstractmethod
    def get_list_of_users(self) -> Iterable[str]:
        ...

    @abstractmethod
    def create_user(self, chat_id: str) -> str:
        ...

    @abstractmethod
    def drop_collection(self) -> None:
        ...


class UserRepositoryStub(UserRepository):
    def create_user(self, chat_id: str) -> str:
        return chat_id

    def get_list_of_users(self) -> Iterable[str]:
        return ["1234"]

    def drop_collection(self) -> None:
        pass


class UserFirebaseRepository(BaseFirebaseRepository, UserRepository):
    db_name: str = "burger-users"

    def __init__(self, credentials: dict[Any, Any]) -> None:
        super().__init__(credentials)
        self.collection = self.client.collection(self.db_name)
        logger.debug("Initialized Firestore repository")

    def _get_users_generator(self) -> Generator[document.DocumentSnapshot, Any, None]:
        return self.collection.stream()

    def get_list_of_users(self) -> Iterable[str]:
        for user in self._get_users_generator():
            logger.debug("Read chat_id {} from the Firestore 🔥", user)
            yield user.id

    def create_user(self, chat_id: str) -> str:
        logger.debug("Creating user with chat_id {}", chat_id)
        self.collection.document(str(chat_id)).set({})
        return str(chat_id)

    def drop_collection(self) -> None:
        logger.debug(
            "Going to delete {} document(-s)", self.collection.count().get()[0][0].value
        )
        for user in self.collection.list_documents():
            user.delete()
