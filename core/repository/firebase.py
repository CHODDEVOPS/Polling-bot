from abc import ABC, abstractmethod
from ast import List

import firebase
import firebase_admin
from firebase_admin import firestore


class BaseFirebaseRepository:
    def __init__(self, credentials: dict) -> None:
        cred = firebase.credentials.Certificate(credentials)
        self.app = firebase_admin.initialize_app(cred)


class UserRepository(ABC):
    @abstractmethod
    def get_list_of_users(self) -> List[str]:
        ...

    @abstractmethod
    def create_user(self, chat_id: str):
        ...


class UserFirebaseRepository(BaseFirebaseRepository, UserRepository):
    db_name: str = "burger-users"

    def __init__(self, credentials: dict) -> None:
        super().__init__(credentials)
        self.client = firestore.client()
        self.collection = firestore.collection(self.db_name)

    def get_list_of_users(self):
        return self.collection.stream()

    def create_user(self, chat_id: int):
        pass
