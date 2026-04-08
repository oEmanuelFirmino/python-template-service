from functools import lru_cache
from domain.services.user_service import UserService
from infrastructure.repositories.user_repo import UserRepository


class Container:

    @staticmethod
    @lru_cache
    def user_repository() -> UserRepository:
        return UserRepository()

    @staticmethod
    @lru_cache
    def user_service() -> UserService:
        return UserService(
            repo=Container.user_repository()
        )